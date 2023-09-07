# Copyright 2023 Nito T.M.
# License https://www.apache.org/licenses/LICENSE-2.0 Apache-2.0
# Author Nito T.M. (https://github.com/nitotm)
# Package pypi.org/project/eld/

from eld import LanguageDetector

detector = LanguageDetector()

# detect() expects a UTF-8 string, returns an object, with a 'language' variable : ISO 639-1 code or null
print(detector.detect('Hola, cómo te llamas?'))
# Object { language: "es", scores(): {"es": 0.53, "et": 0.21, ...}, is_reliable(): True }
# Object { language: None|str, scores(): None|dict, is_reliable(): bool }
print(detector.detect('Hola, cómo te llamas?').language)
# "es"

# clean_text(True) Removes Urls, domains, emails, alphanumerical & numbers
detector.clean_text(True)  # Default is False

# To reduce the languages to be detected, there are 3 different options, they only need to be executed once.
# This is the complete list on languages for ELD v1, using ISO 639-1 codes:
# ['am', 'ar', 'az', 'be', 'bg', 'bn', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gu',
# 'he', 'hi', 'hr', 'hu', 'hy', 'is', 'it', 'ja', 'ka', 'kn', 'ko', 'ku', 'lo', 'lt', 'lv', 'ml', 'mr', 'ms', 'nl',
# 'no', 'or', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur',
# 'vi', 'yo', 'zh']

lang_subset = ['en', 'es', 'fr', 'it', 'nl', 'de']

# Option 1. With dynamic_lang_subset(), detect() executes normally, but at the end will filter the excluded languages.
detector.dynamic_lang_subset(lang_subset)
# Returns an object with a list named 'languages', with the validated languages or 'None'

# to remove the subset
detector.dynamic_lang_subset(None)

# Option 2. lang_subset(langs,save=True) Will previously remove the excluded languages form the Ngrams database; for
# a single detection might be slower than dynamic_lang_subset(), but for several strings will be faster. If 'save'
# option is true (default), the new ngrams subset will be stored and cached for next time.
detector.lang_subset(lang_subset)
# Returns object {success: True, languages: ['de', 'en', ...], error: None, file: 'ngramsM60...'}

# to remove the subset
detector.lang_subset(None)

print(detector.VERSION)

# Finally the optimal way to regularly use the same language subset, will be to add as an argument the file stored
# (and returned) by lang_subset(), when creating an instance of the class. In this case the subset Ngrams database will
# be loaded directly, and not the default database. Also, you can use this option to load different ngram databases
# stored at eld/resources/ngrams
langSubsetDetect = LanguageDetector('ngramsM60-6_5ijqhj4oecs310zqtm8u9pgmd9ox2yd')
