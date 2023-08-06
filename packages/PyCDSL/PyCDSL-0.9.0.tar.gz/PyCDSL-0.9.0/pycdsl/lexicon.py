#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDSL Lexicon Management
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, field
from functools import lru_cache
import zipfile
from typing import Dict, Generator, List

from peewee import fn
from playhouse.db_url import connect

import bs4
import requests
from requests_downloader.downloader import download
from indic_transliteration.sanscript import transliterate

from .utils import validate_scheme, validate_search_mode
from .models import (
    Lexicon, Entry,
    lexicon_constructor, entry_constructor
)
from .constants import (
    INTERNAL_SCHEME,
    ENGLISH_DICTIONARIES,
    DEFAULT_SEARCH_MODE,
    SEARCH_MODE_KEY,
    SEARCH_MODE_VALUE,
    SEARCH_MODE_BOTH
)

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################


@dataclass(eq=False)
class CDSLDict:
    """Dictionary from CDSL"""
    id: str
    date: str
    name: str
    url: str = field(repr=False)
    db: str = field(repr=False, default=None)
    search_mode: str = field(repr=False, default=None)
    input_scheme: str = field(repr=False, default=None)
    output_scheme: str = field(repr=False, default=None)
    transliterate_keys: bool = field(repr=False, default=None)

    # ----------------------------------------------------------------------- #

    def __post_init__(self):
        self.set_scheme(
            input_scheme=self.input_scheme,
            output_scheme=self.output_scheme,
            transliterate_keys=self.transliterate_keys
        )
        self.set_search_mode(self.search_mode)

    # ----------------------------------------------------------------------- #

    def __getitem__(self, item: str) -> Entry:
        result = self.entry(item)
        if result is None:
            raise KeyError(f"Entry with ID '{item}' not found.")
        else:
            return result

    def __iter__(self) -> Generator[Entry, None, None]:
        for entry in self._lexicon.select():
            yield self._entry(
                entry,
                lexicon_id=self.id,
                scheme=self.output_scheme,
                transliterate_keys=self.transliterate_keys
            )

    # ----------------------------------------------------------------------- #

    def download(self, download_dir: str or Path) -> bool:
        """Download and extract dictionary data

        Parameters
        ----------
        download_dir : str or Path
            Full path of directory where the dictionary data should be
            downloaded and extracted

        Returns
        -------
        bool
            True if successfully downloaded or already up-to-date
        """
        up_to_date = False

        html = requests.get(self.url).content.decode()
        soup = bs4.BeautifulSoup(html, "html.parser")
        footer = soup.find("div", attrs={"id": "footer"})
        last_modified = footer.find("p").get_text().split(":", 1)[-1].strip()
        LOGGER.debug(f"Last modified at {last_modified}")

        download_dir = Path(download_dir)
        download_dir.mkdir(parents=True, exist_ok=True)

        last_modified_file = download_dir / "last_modified.txt"

        if last_modified_file.exists():
            local_last_modified = last_modified_file.read_text().strip()
            up_to_date = (local_last_modified == last_modified)

        if not up_to_date:
            # not up-to-date
            # backup current file
            download_path = download_dir / f"{self.id}.web.zip"
            backup_path = download_dir / f"{self.id}.web.zip.bak"
            if download_path.exists():
                backup_path = download_path.rename(backup_path)

            # find download link
            lis = soup.find_all("li")
            for li in lis:
                if "Directory 'web' containing displays" in li.get_text():
                    break
            else:
                LOGGER.error("No download link for 'web' displays was found.")
                return False

            web_url = li.find("a")["href"]
            web_url = requests.compat.urljoin(self.url, web_url)

            # download
            success = download(web_url, download_path=download_path)

            if not success:
                # download failed - restore backup
                LOGGER.error("Something went wrong.")
                if backup_path.exists():
                    LOGGER.debug("Restoring ..")
                    backup_path.rename(download_path)
                return False

            # download was sucessful - remove backup
            if backup_path.exists():
                backup_path.unlink()

            # update last modified info
            last_modified_file.write_text(last_modified)

            # extract
            with zipfile.ZipFile(download_path, "r") as zipref:
                zipref.extractall(download_dir)
        else:
            LOGGER.info(f"Data for dictionary '{self.id}' is up-to-date.")
        return True

    def setup(
        self,
        data_dir: str or Path,
        symlink_dir: str or Path = None,
        update: bool = False
    ) -> bool:
        """Setup the dictionary database path

        Parameters
        ----------
        data_dir : str or Path
            Full path of directory where the dictionary data is stored
        symlink_dir : str or Path, optional
            Full path of the directory where the symbolink links to the
            SQLite database of dictionary will be created
            If None, symbolic links aren't created.
            The default is None.
        update : bool, optional
            If True, an attempt to update dictionary data will be made.
            The default is False.

        Returns
        -------
        bool
            True if the setup was successful
        """
        # setup database path
        data_dir = Path(data_dir)
        database_filename = f"{self.id.lower()}.sqlite"
        database_path = data_dir / "web" / "sqlite" / database_filename
        self.db = str(database_path)

        status = (
            (not update and database_path.exists())
            or
            self.download(download_dir=data_dir)
        )
        if not status:
            LOGGER.error(f"Couldn't setup dictionary '{self.id}'.")
            return False

        # create symlink
        if symlink_dir is not None:
            symlink_dir = Path(symlink_dir)
            symlink_dir.mkdir(parents=True, exist_ok=True)
            symlink_path = symlink_dir / f"{self.id}.db"
            if not symlink_path.exists():
                symlink_path.symlink_to(database_path)
            self.db = str(symlink_path)

        return True

    # ----------------------------------------------------------------------- #

    def set_scheme(
        self,
        input_scheme: str = None,
        output_scheme: str = None,
        transliterate_keys: bool = None
    ):
        """Set transliteration scheme for the dictionary instance

        Parameters
        ----------
        input_scheme : str, optional
            Input transliteration scheme.
            If None, `INTERNAL_SCHEME` is used.
            The default is None.
        output_scheme : str, optional
            Output transliteration scheme.
            If None, `INTERNAL_SCHEME` is used.
            The default is None.
        transliterate_keys : bool, optional
            Determines whether the keys in lexicon should be transliterated
            to `scheme` or not.
            If None, the value will be inferred based on dictionary type.
            The default is None.
        """
        input_scheme = validate_scheme(input_scheme) or INTERNAL_SCHEME
        output_scheme = validate_scheme(output_scheme) or INTERNAL_SCHEME
        if transliterate_keys is None:
            transliterate_keys = (self.id in ENGLISH_DICTIONARIES)

        if (
            self.input_scheme != input_scheme or
            self.output_scheme != output_scheme or
            self.transliterate_keys != transliterate_keys
        ):
            self.search.cache_clear()
            self.stats.cache_clear()

        self.input_scheme = input_scheme
        self.output_scheme = output_scheme
        self.transliterate_keys = transliterate_keys

    def set_search_mode(self, mode: str):
        """Set search mode

        Parameters
        ----------
        mode : str
            Valid values are 'key', 'value', 'both'
            Recommended to use the convenience variables SEARCH_MODE_KEY,
            SEARCH_MODE_VALUE or SEARCH_MODE_BOTH.
        """
        self.search_mode = validate_search_mode(mode) or DEFAULT_SEARCH_MODE

    # ----------------------------------------------------------------------- #

    def connect(
        self,
        lexicon_model: Lexicon = None,
        entry_model: Entry = None
    ):
        """
        Connect to the SQLite database

        If both `lexicon_model` and `entry_model` are specified,
        they are used as the ORM layer, and take preference over `model_map`.

        If any of `lexicon_model` or `entry_model` is None,
        then the models are resolved in the following way.

        First, if the current dictionary ID is present in `model_map` the
        models specified by the `model_map` are used.
        Otherwise, `models.lexicon_constructor` and `models.entry_constructor`
        functions are used, which subclass the `models.Lexicon` and
        `models.Entry` models.

        Parameters
        ----------
        lexicon_model : object, optional
            Lexicon model.
            The default is None.
        entry_model : object, optional
            Entry model.
            The default is None.
        """
        if lexicon_model is not None and entry_model is not None:
            self._lexicon = lexicon_model
            self._entry = entry_model
        else:
            self._lexicon = lexicon_constructor(self.id)
            self._entry = entry_constructor(self.id)

        db_url = f"sqlite:///{self.db}"
        self._lexicon.bind(connect(db_url))
        self.search.cache_clear()
        self.stats.cache_clear()

    # ----------------------------------------------------------------------- #

    @lru_cache(maxsize=1)
    def stats(self, top: int = 10, output_scheme: str = None) -> Dict:
        """Display statistics about the lexicon

        Parameters
        ----------
        top : int, optional
            Display top `top` entries having most different meanings.
            The default is 10.
        output_scheme: str, optional
            Output transliteration scheme
            If None, `self.output_scheme` will be used.
            The default is None.

        Returns
        -------
        dict
            Statistics about the dictionary
        """
        output_scheme = validate_scheme(output_scheme) or self.output_scheme
        lex = self._lexicon
        total_count = lex.select().count()
        distinct_query = (
            lex
            .select(
                lex.id, lex.key, lex.data, fn.COUNT(lex.key).alias("count")
            )
            .group_by(lex.key)
            .order_by(fn.COUNT(lex.key).desc())
        )
        top_entries = [
            (
                (
                    transliterate(
                        item.key,
                        INTERNAL_SCHEME,
                        output_scheme
                    ) if self.transliterate_keys else item.key
                ),
                item.count
            )
            for item in distinct_query.limit(top)
        ]
        distinct_count = distinct_query.count()
        return {
            "total": total_count,
            "distinct": distinct_count,
            "top": top_entries
        }

    # ----------------------------------------------------------------------- #

    @lru_cache(maxsize=4096)
    def search(
        self,
        pattern: str,
        mode: str = None,
        input_scheme: str = None,
        output_scheme: str = None,
        ignore_case: str = False,
        limit: int = None,
        offset: int = None
    ) -> List[Entry]:
        """Search in the dictionary

        Parameters
        ----------
        pattern : str
            Search pattern, may contain wildcards (`*`).
        mode : str or None, optional
            Search mode to query by `key`, `value` or `both`.
            If None, `self.search_mode` will be used.
            The default is None.
        input_scheme : str or None, optional
            Input transliteration scheme
            If None, `self.input_scheme` will be used.
            The default is None.
        output_scheme : str or None, optional
            Output transliteration scheme
            If None, `self.output_scheme` will be used.
            The default is None.
        ignore_case : bool, optional
            Ignore case while performing lookup.
            The default is False.
        limit : int or None, optional
            Limit the number of search results to `limit`.
            The default is None.
        offset : int or None, optional
            Offset the search results by `offset`.
            The default is None

        Returns
        -------
        list
            List of matching entries
        """
        input_scheme = validate_scheme(input_scheme) or self.input_scheme
        output_scheme = validate_scheme(output_scheme) or self.output_scheme
        mode = validate_search_mode(mode) or self.search_mode

        pattern = transliterate(pattern, input_scheme, INTERNAL_SCHEME)
        value_pattern = f"*<body>*{pattern.strip('*')}*</body>*"

        if mode == SEARCH_MODE_KEY:
            query = self._lexicon.select().where(self._lexicon.key % pattern)
            iquery = self._lexicon.select().where(self._lexicon.key ** pattern)
        if mode == SEARCH_MODE_VALUE:
            query = self._lexicon.select().where(
                self._lexicon.data % value_pattern
            )
            iquery = self._lexicon.select().where(
                self._lexicon.data ** value_pattern
            )
        if mode == SEARCH_MODE_BOTH:
            query = self._lexicon.select().where(
                (self._lexicon.key % pattern) |
                (self._lexicon.data % value_pattern)
            )
            iquery = self._lexicon.select().where(
                (self._lexicon.key ** pattern) |
                (self._lexicon.data ** value_pattern)
            )

        search_query = iquery if ignore_case else query
        return [
            self._entry(
                result,
                lexicon_id=self.id,
                scheme=output_scheme,
                transliterate_keys=self.transliterate_keys
            )
            for result in search_query.limit(limit).offset(offset)
        ]

    def entry(self, entry_id: str, output_scheme: str = None) -> Entry or None:
        """Get an entry by ID

        Parameters
        ----------
        entry_id : str
            Entry ID to lookup
        output_scheme : str or None, optional
            Output transliteration scheme
            If None, `self.output_scheme` will be used.
            The default is None.

        Returns
        -------
        object
            If the `entry_id` is valid, `Entry` with the matching ID
            otherwise, None.
        """

        output_scheme = validate_scheme(output_scheme) or self.output_scheme
        try:
            return self._entry(
                self._lexicon.get(self._lexicon.id == entry_id),
                lexicon_id=self.id,
                scheme=output_scheme,
                transliterate_keys=self.transliterate_keys
            )
        except Exception:
            LOGGER.error(f"Entry with ID '{entry_id}' not found.")

    def dump(
        self,
        output_path: str or Path = None,
        output_scheme: str = None
    ) -> List[Dict[str, str]]:
        """
        Dump data as JSON

        Parameters
        ----------
        output_path : str or Path, optional
            Path to the output JSON file.
            If None, the data isn't written to the disk, only returned.
            The default is None.
        output_scheme : str or None, optional
            Output transliteration scheme
            If None, `self.output_scheme` will be used.
            The default is None

        Returns
        -------
        list
            List of all the entries in the dictionary. Every entry is a `dict`.
            If `output_path` is provided, the same list is written as JSON.
        """
        output_scheme = validate_scheme(output_scheme) or self.output_scheme
        data = [
            entry.to_dict()
            for entry in (
                self._entry(
                    result,
                    lexicon_id=self.id,
                    scheme=output_scheme,
                    transliterate_keys=self.transliterate_keys
                )
                for result in self._lexicon.select()
            )
        ]
        if output_path is not None:
            with open(output_path, mode="w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
        return data


###############################################################################
