# Copyright 2023 Nito T.M.
# License https://www.apache.org/licenses/LICENSE-2.0 Apache-2.0
# Author Nito T.M. (https://github.com/nitotm)
# Package pypi.org/project/eld/

import hashlib
import os
import copy
import importlib.util
import logging

from eld.languageData import languageData
from eld.subsetResult import SubsetResult


class LanguageSubset:

    def __init__(self):
        self.subset = None
        self.default_ngrams = None
        self.loaded_subset = None

    def dynamic_lang_subset(self, languages):
        """
        Sets a subset, then detect() will filter the languages not included, from the scores with filterLangSubset()
        Call dynamic_lang_subset(None) to deactivate

        Args:
            languages (list or None): List of languages (ISO 639-1) to include in subset, or None to delete subset

        Returns:
            object SubsetResult: success (bool), languages (list or None), error (str or None)
        """
        self.subset = None
        if languages:
            self.subset = _make_subset(languages)
            if self.subset is None:
                return SubsetResult(False, None, 'No language matched this set')
        return SubsetResult(True, _iso_languages(self.subset) if self.subset else None)

    def lang_subset(self, languages, save=True):
        """
         Sets a subset and removes the excluded languages form the ngrams database
         if $save option is true, the new ngrams subset will be stored, and cached for next time

        Args:
            languages (list or None): List of languages (ISO 639-1) to include in subset, or None to delete subset

        Returns:
            object SubsetResult: success (bool), languages (list or None), error (str or None), file (str)
        """
        if not languages:
            if self.loaded_subset and self.default_ngrams:
                languageData.ngrams = copy.deepcopy(self.default_ngrams)
                self.loaded_subset = None
            return SubsetResult(True)  # if there was already no subset to disable, it also is successful

        lang_array = _make_subset(languages)
        if not lang_array:
            return SubsetResult(False, None, 'No language matched this set')

        if self.default_ngrams is None:
            self.default_ngrams = copy.deepcopy(languageData.ngrams)

        langs_str = [str(lang) for lang in lang_array]
        new_subset = base16_to_base36(
            hashlib.sha1(','.join(langs_str).encode()).hexdigest()
        )
        file_name = 'ngrams' + languageData.type + '-' + str(len(lang_array)) + '_' + new_subset
        file_path = languageData.folder + 'subset/' + file_name + '.py'

        if self.loaded_subset != new_subset:
            self.loaded_subset = new_subset

            if os.path.exists(file_path):
                # module = importlib.import_module('.ngrams.' + file_name, package=file_name)
                spec = importlib.util.spec_from_file_location(file_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                languageData.ngrams = module.ngrams_data['ngrams']
                if languageData.ngrams:
                    return SubsetResult(True, _iso_languages(lang_array), None, file_path)

            if self.default_ngrams != languageData.ngrams:
                languageData.ngrams = copy.deepcopy(self.default_ngrams)

            for ngram, langsID in self.default_ngrams.items():
                for lid, value in langsID.items():
                    if lid not in lang_array:
                        del languageData.ngrams[ngram][lid]
                if not languageData.ngrams[ngram]:
                    del languageData.ngrams[ngram]

        saved = False
        if save:
            saved = _save_ngrams(file_path, lang_array)

        return SubsetResult(True, _iso_languages(lang_array), None, (file_name if saved else None))

    def _filter_lang_subset(self, scores):
        """Filters languages not included in the subset, from the result scores"""
        sub_results = []
        for score in scores:
            if score[0] in self.subset:
                sub_results.append(score)
        return sub_results


def _ngram_export(data):
    if isinstance(data, dict):
        to_implode = []
        for key, value in data.items():
            to_implode.append(repr(key) + ':' + _ngram_export(value))
        code = '{' + ','.join(to_implode) + '}'
        return code
    else:
        return repr(data)


def _save_ngrams(file_path, lang_array):
    if not os.path.exists(file_path):  # in case self.loaded_subset != new_subset, and was previously saved
        try:
            with open(file_path, 'w') as f:
                f.write(
                    '# Copyright 2023 Nito T.M. [ Apache 2.0 Licence https://www.apache.org/licenses/LICENSE-2.0 ]\n' +
                    'ngrams_data = {\n' +
                    '   "type": "' + str(languageData.type) + '",\n' +
                    '   "languages": ' + str(_iso_languages(lang_array)) + ',\n' +
                    '   "is_subset": True,\n' +
                    '   "ngrams": ' + _ngram_export(languageData.ngrams) + '\n' +
                    '}')
        except Exception as e:
            logging.exception(e)
            return False
    return True


def _make_subset(languages):
    """
    Validates an expected array of ISO 639-1 language code strings, given by the user, and creates a subset of the valid
    languages compared against the current database available languages
    """
    subset = []
    reverse_langs = {v: k for k, v in languageData.lang_codes.items()}
    if languages:
        for lang in languages:
            found_lang = reverse_langs.get(lang)
            if found_lang is not None:
                subset.append(found_lang)
        subset.sort()
    return subset or None


def _iso_languages(lang_set):
    """Converts ngram database language indexes (integer) to ISO 639-1 code"""
    lang_codes = {}
    for lang_id in lang_set:
        lang_codes[lang_id] = languageData.lang_codes[lang_id]
    return lang_codes


def base16_to_base36(hex_string):
    # Convert hex string to integer
    integer_value = int(hex_string, 16)
    # Convert integer to base-36 string
    base36_string = ''
    while integer_value > 0:
        integer_value, remainder = divmod(integer_value, 36)
        base36_digit = '0123456789abcdefghijklmnopqrstuvwxyz'[remainder]
        base36_string = base36_digit + base36_string

    return base36_string
