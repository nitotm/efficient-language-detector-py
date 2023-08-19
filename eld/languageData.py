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

import importlib.util
import os


class LanguageData:
    def __init__(self):
        from .resources.avg_score import avg_score
        self.avg_score = avg_score
        self.ngrams = {}
        self.lang_score = []
        self.lang_codes = {}
        self.type = ''
        self.folder = os.path.dirname(__file__) + '/resources/ngrams/'

    """ 
    ISO 639-1 codes, for the 60 languages set.
    ['am', 'ar', 'az', 'be', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gu',
    'he', 'hi', 'hr', 'hu', 'hy', 'is', 'it', 'ja', 'ka', 'kn', 'ko', 'ku', 'lo', 'lt', 'lv', 'ml', 'mr', 'ms', 'nl',
    'no', 'or', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur',
    'vi', 'yo', 'zh']
          
    ['Amharic', 'Arabic', 'Azerbaijani (Latin)', 'Belarusian', 'Bulgarian', 'Bengali', 'Catalan', 'Czech', 'Danish',
    'German', 'Greek', 'English', 'Spanish', 'Estonian', 'Basque', 'Persian', 'Finnish', 'French', 'Gujarati', 'Hebrew',
    'Hindi', 'Croatian', 'Hungarian', 'Armenian', 'Icelandic', 'Italian', 'Japanese', 'Georgian', 'Kannada', 'Korean',
    'Kurdish (Arabic)', 'Lao', 'Lithuanian', 'Latvian', 'Malayalam', 'Marathi', 'Malay (Latin)', 'Dutch', 'Norwegian',
    'Oriya', 'Punjabi', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Slovak', 'Slovene', 'Albanian',
    'Serbian (Cyrillic)', 'Swedish', 'Tamil', 'Telugu', 'Thai', 'Tagalog', 'Turkish', 'Ukrainian', 'Urdu', 'Vietnamese',
    'Yoruba', 'Chinese']
    """

    def load_ngrams(self, subset_file=''):
        if subset_file == '':
            from .resources.ngrams.ngramsM60 import ngrams_data
        else:
            # module = importlib.import_module('.ngrams.' + subset_file)
            file_path = self.folder + subset_file + '.py'
            if not os.path.exists(file_path):
                file_path = self.folder + 'subset/' + subset_file + '.py'
            spec = importlib.util.spec_from_file_location(subset_file, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            ngrams_data = module.ngrams_data

        self.ngrams = ngrams_data['ngrams']
        self.lang_score = [0] * (max(ngrams_data['languages'].keys()) + 1)
        self.type = ngrams_data['type']
        self.lang_codes = ngrams_data['languages']


languageData = LanguageData()
