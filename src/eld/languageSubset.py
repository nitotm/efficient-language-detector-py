"""
Copyright 2023 Nito T.M.
Author URL: https://github.com/nitotm

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import hashlib
import os
import copy
import importlib.util

from .languageData import languageData

"""
To reduce the languages to be detected, there are 3 different options, they only need to be execute once.

The fastest option to regularly use the same language subset, will be to add as an argument the file stored 
(and returned) by lang_subset(), when creating an instance of the languageDetector class. 
  In this case the subset ngrams database will be loaded directly, and not the default database. 
  Also you can use this option to load different ngram databases.
"""


class LanguageSubset:

    # dynamic_lang_subset() Will execute the detector normally, but at the end it will filter the excluded languages.
    def dynamic_lang_subset(self, langs):
        self.subset = []
        if not langs:
            langs = []
        for value in langs:
            if value in languageData.langCodes:
                self.subset.append(languageData.langCodes.index(value))
        self.subset.sort()
        return self.subset

    """ lang_subset(langs,save=true) Will previously remove the excluded languages form the ngrams database; for a
     single detection might be slower than dynamic_lang_subset(), but for multiple strings will be faster. if 'save' 
     option is true (default), the new ngrams subset will be stored, and next loaded for the same languages subset,
     increasing startup speed.
    """
    def lang_subset(self, langs, save=True):
        if not langs:
            if self.loadedSubset:
                languageData.ngrams = copy.deepcopy(self.defaultNgrams)
                self.loadedSubset = False
            return True
        
        langs_array = self.dynamic_lang_subset(langs)
        if not langs_array:
            return 'No languages found'
        self.subset = False  # We use dynamic_lang_subset() to filter languages, but set dynamic subset to false
        if self.defaultNgrams is False:
            self.defaultNgrams = copy.deepcopy(languageData.ngrams)

        langs_str = [str(lang) for lang in langs_array]
        new_subset = hashlib.sha1(','.join(langs_str).encode()).hexdigest()
        file_name = 'ngrams_' + new_subset
        file_path = os.path.dirname(__file__)+'/ngrams/' + file_name + '.py'

        if self.loadedSubset != new_subset:
            self.loadedSubset = new_subset

            if os.path.exists(file_path):
                # module = importlib.import_module('.ngrams.' + file_name, package=file_name)
                spec = importlib.util.spec_from_file_location(file_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                languageData.ngrams = module.ngrams
                return

            if self.defaultNgrams != languageData.ngrams:
                languageData.ngrams = copy.deepcopy(self.defaultNgrams)

            for ngram, langsID in self.defaultNgrams.items():
                for lid, value in langsID.items():
                    if lid not in langs_array:
                        del languageData.ngrams[ngram][lid]
                if not languageData.ngrams[ngram]:
                    del languageData.ngrams[ngram]

        if save:
            if not os.path.exists(file_path):  # in case self.loadedSubset != new_subset, and was previously saved
                with open(file_path, 'w') as f:
                    f.write('ngrams = ' + self.ngram_export(languageData.ngrams))
            return file_path

        return True

    def filter_lang_subset(self, results):
        sub_results = []
        for value in results:
            if value[0] in self.subset:
                sub_results.append(value)
        return sub_results

    def ngram_export(self, var, safe=False):
        if isinstance(var, dict):
            to_implode = []
            for key, value in var.items():
                to_implode.append('b\'\\x' + ''.join(chunk_split(bin2hex(key), 2, '\\x')[:-2]) + '\'' if safe else repr(
                    key) + ':' + self.ngram_export(value))
            code = '{' + ','.join(to_implode) + '}'
            return code
        else:
            return repr(var)
