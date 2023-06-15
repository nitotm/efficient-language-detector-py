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

from src.eld.languageDetector import LanguageDetector
# from eld import LanguageDetector

detector = LanguageDetector()

# detect() expects a UTF-8 string, and returns a dictionary, with key 'language', value: ISO 639-1 code or false
print(detector.detect('Hola, cómo te llamas?'))
# {'language': 'es'}
# {'language': False, 'error': 'Some error', 'scores': {}}

# To get the best guess, turn off minimum length and confidence threshold; also used for benchmarking.
print(detector.detect('To', False, False, 0, 1))

# To improve readability Named Parameters can be used
detector.detect(text='To', clean_text=False, check_confidence=False, min_byte_length=0, min_ngrams=1)
# clean_text=True, Removes Urls, domains, emails, alphanumerical & numbers

# To retrieve the scores of all languages detected, we will set returnScores to True, just once
detector.return_scores = True
print(detector.detect('How are you? Bien, gracias'))
# {'language': 'en', 'scores': {'en': 0.32, 'es': 0.31, ...}}

# To reduce the languages to be detected, there are 3 different options, they only need to be executed once.
# This is the complete list on languages for ELD v1, using ISO 639-1 codes:
""" ['am', 'ar', 'az', 'be', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gu',
 'he', 'hi', 'hr', 'hu', 'hy', 'is', 'it', 'ja', 'ka', 'kn', 'ko', 'ku', 'lo', 'lt', 'lv', 'ml', 'mr', 'ms', 'nl', 'no',
 'or', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'yo',
 'zh']
"""
lang_subset = ['en', 'es', 'fr', 'it', 'nl', 'de']

# dynamic_lang_subset() Will execute the detector normally, but at the end will filter the excluded languages.
detector.dynamic_lang_subset(lang_subset)

# to remove the subset
detector.dynamic_lang_subset(False)

""" lang_subset(langs,save=True) Will previously remove the excluded languages form the Ngrams database; for a single
 detection might be slower than dynamic_lang_subset(), but for several strings will be faster. If save option is true
(default), the new ngrams subset will be stored, and loaded for the same languages subset, increasing startup speed
"""
detector.lang_subset(lang_subset)

# to remove the subset
detector.lang_subset(False)

""" Finally the fastest option to regularly use the same language subset, will be to add as an argument the file 
   stored by lang_subset(), when creating an instance of the class. In this case the subset Ngrams database will
   be loaded directly, and not the default database. Also, you can use this option to load different ngram databases
   stored at src/ngrams/
"""
langSubsetDetect = LanguageDetector('ngrams_2f37045c74780aba1d36d6717f3244dc025fb935')
