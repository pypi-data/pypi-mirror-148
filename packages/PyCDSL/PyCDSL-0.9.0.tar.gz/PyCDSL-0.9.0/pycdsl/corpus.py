#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CDSL Corpus Management
"""

###############################################################################

import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Generator, List, Tuple

import bs4
import requests

from .models import (
    Lexicon, Entry,
    MWLexicon, MWEntry,
    AP90Lexicon, AP90Entry
)
from .lexicon import CDSLDict
from .constants import (
    DEFAULT_SEARCH_MODE,
    SERVER_URL,
    DEFAULT_CORPUS_DIR,
    DEFAULT_DICTIONARIES,
    ENGLISH_DICTIONARIES,
    DEFAULT_SCHEME,
)

###############################################################################

DEFAULT_MODEL_MAP = {
    "MW": (MWLexicon, MWEntry),
    "AP90": (AP90Lexicon, AP90Entry),
}

###############################################################################

LOGGER = logging.getLogger(__name__)

###############################################################################


@dataclass
class CDSLCorpus:
    """
    CDSL Corpus Class

    Refers to a CDSL installation instance at the location `data_dir`.
    """
    data_dir: str or Path = field(default=None)
    search_mode: str = field(repr=False, default=DEFAULT_SEARCH_MODE)
    input_scheme: str = field(repr=False, default=DEFAULT_SCHEME)
    output_scheme: str = field(repr=False, default=DEFAULT_SCHEME)
    transliterate_keys: bool = field(repr=False, default=True)

    # ----------------------------------------------------------------------- #

    def __post_init__(self):
        self.data_dir = (
            Path(DEFAULT_CORPUS_DIR)
            if self.data_dir is None
            else Path(self.data_dir)
        )
        self.dict_dir = self.data_dir / "dict"
        self.db_dir = self.data_dir / "db"
        self.dicts = {}
        self.get_available_dicts()

    # ----------------------------------------------------------------------- #

    def __getattr__(self, attr: str) -> CDSLDict:
        if attr in self.dicts:
            return self.dicts[attr]
        else:
            raise AttributeError

    def __getitem__(self, item: str) -> CDSLDict:
        if item in self.dicts:
            return self.dicts[item]
        else:
            raise KeyError(f"Dictionary '{item}' is not setup.")

    def __iter__(self) -> Generator[CDSLDict, None, None]:
        yield from self.dicts.values()

    # ----------------------------------------------------------------------- #

    def setup(
        self,
        dict_ids: list = None,
        update: bool = False,
        model_map: Dict[str, Tuple[Lexicon, Entry]] = None
    ) -> bool:
        """Setup CDSL dictionaries in bulk

        Calls `CDSLDict.setup()` on every `CDSLDict`, and if successful, also
        calls `CDSLDict.connect()` to establish a connection to the database

        Parameters
        ----------
        dict_ids : list or None, optional
            List of dictionary IDs to setup.
            If None, the dictionaries from `DEFAULT_DICTIONARIES` as well as
            locally installed dictionaries will be setup.
            The default is None.
        update : bool, optional
            If True, and update check is performed for every dictionary in
            `dict_ids`, and if available, the updated version is installed
            The default is False.
        lexicon_model : object, optional
            Lexicon model argument passed to `CDSLDict.connect()`
            The default is None.
        entry_model : object, optional
            Entry model argument passed to `CDSLDict.connect()`
            The default is None.
        model_map : dict, optional
            Map of dictionary ID to a tuple of lexicon model and entry model.
            The argument is used to specify `lexicon_model` and `entry_model`
            arguments passed to `CDSLDict.connect()`.
            If None, the default map `DEFAULT_MODEL_MAP` will be used.
            The default is None.

        Returns
        -------
        bool
            True, if the setup of all the dictionaries from `dict_ids`
            is successful.
            i.e. If every `CDSLDict.setup()` call returns True.

        Raises
        ------
        ValueError
            If `dict_ids` is not a `list` or `None`.
        """
        if dict_ids is None:
            dict_ids = DEFAULT_DICTIONARIES + list(self.get_installed_dicts())

        if isinstance(dict_ids, list):
            dict_ids = {dict_id.upper() for dict_id in dict_ids}
            setup_dicts = {
                dict_id: cdsl_dict
                for dict_id, cdsl_dict in self.available_dicts.items()
                if dict_id in dict_ids
            }
        else:
            raise ValueError("`dict_ids` must be a `list` or `None`")

        status = []
        for dict_id, cdsl_dict in setup_dicts.items():
            dict_dir = self.dict_dir / dict_id.upper()
            success = cdsl_dict.setup(
                data_dir=dict_dir,
                symlink_dir=self.db_dir,
                update=update
            )
            status.append(success)
            if success:
                if model_map is None:
                    model_map = DEFAULT_MODEL_MAP

                lexicon_model, entry_model = model_map.get(
                    cdsl_dict.id,
                    (None, None)
                )

                cdsl_dict.connect(
                    lexicon_model=lexicon_model,
                    entry_model=entry_model
                )
                self.dicts[dict_id] = cdsl_dict

        return bool(status) and all(status)

    # ----------------------------------------------------------------------- #

    def search(
        self,
        pattern: str,
        dict_ids: List[str] = None,
        mode: str = None,
        input_scheme: str = None,
        output_scheme: str = None,
        ignore_case: bool = False,
        limit: int = None,
        offset: int = None,
        omit_empty: bool = True
    ) -> Dict[str, List[Entry]]:
        """Search in multiple dictionaries from the corpus

        Parameters
        ----------
        pattern : str
            Search pattern, may contain wildcards (`*`).
        dict_ids : list or None
            List of dictionary IDs to search in.
            Only the `dict_ids` that exist in `self.dicts` will be used.
            If None, all the dictionaries that have been setup,
            i.e., the dictionaries from `self.dicts` will be used.
            The default is None.
        mode : str or None, optional
            Search mode to query by `key`, `value` or `both`.
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
        omit_empty : bool, optional
            If True, only the non-empty search results will be included.
            The default is False.

        Returns
        -------
        dict
            Dictionary of (dict_id, list of matching entries)
        """
        all_results = {}

        if dict_ids is None:
            dict_ids = list(self.dicts)

        if isinstance(dict_ids, list):
            dict_ids = {
                dict_id.upper()
                for dict_id in dict_ids
                if dict_id.upper() in self.dicts
            }
        else:
            raise ValueError("`dict_ids` must be a `list` or `None`")

        for dict_id in dict_ids:
            dict_results = self.dicts[dict_id].search(
                pattern=pattern,
                mode=mode,
                input_scheme=input_scheme,
                output_scheme=output_scheme,
                ignore_case=ignore_case,
                limit=limit,
                offset=offset
            )

            if not omit_empty or dict_results:
                all_results[dict_id] = dict_results

        return all_results

    # ----------------------------------------------------------------------- #

    def get_available_dicts(self) -> Dict[str, CDSLDict]:
        """
        Fetch a list of dictionaries available for download from CDSL

        Homepage of CDSL Project (`SERVER_URL`) is fetched and parsed to obtain
        this list.
        """
        html = requests.get(SERVER_URL).content.decode()
        soup = bs4.BeautifulSoup(html, "html.parser")
        dl_tags = soup.find_all("a", attrs={"title": "Downloads"})
        dictionaries = {}
        for dl_tag in dl_tags:
            row = dl_tag.find_parent("tr")
            cells = row.find_all("td")
            assert(len(cells) == 4)
            dict_id = cells[0].get_text(" ").strip().split()[0]
            dict_date = cells[1].get_text(" ").strip().split()[0]
            dict_name = cells[2].find("a").get_text(" ").strip()
            dict_download = f"{SERVER_URL}{dl_tag['href']}"
            dict_transliterate_keys = (
                dict_id not in ENGLISH_DICTIONARIES
                and
                self.transliterate_keys
            )

            dictionaries[dict_id] = CDSLDict(
                id=dict_id,
                date=dict_date,
                name=dict_name,
                url=dict_download,
                search_mode=self.search_mode,
                input_scheme=self.input_scheme,
                output_scheme=self.output_scheme,
                transliterate_keys=dict_transliterate_keys
            )

        self.available_dicts = dictionaries
        return dictionaries

    # ----------------------------------------------------------------------- #

    def get_installed_dicts(self) -> Dict[str, CDSLDict]:
        """Fetch a list of dictionaries installed locally"""
        dictionaries = {}
        dict_ids = [path.name for path in self.dict_dir.glob("*")]
        for dict_id in dict_ids:
            if dict_id not in self.available_dicts:
                LOGGER.error(f"Invalid dictionary '{dict_id}'")
                continue

            db_filename = f"{dict_id.lower()}.sqlite"
            db_path = self.dict_dir / dict_id / "web" / "sqlite" / db_filename
            if db_path.is_file():
                dictionaries[dict_id] = self.available_dicts[dict_id]

        return dictionaries

###############################################################################
