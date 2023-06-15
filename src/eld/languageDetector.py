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

import regex as re

from .languageData import languageData
from .languageSubset import LanguageSubset


class LanguageDetector(LanguageSubset):
    def __init__(self, subset_file=''):
        self.return_scores = False
        LanguageSubset.subset = False
        LanguageSubset.loadedSubset = False
        LanguageSubset.defaultNgrams = False
        languageData.load_ngrams(subset_file)

    """
      detect() returns a dictionary, with a value named 'language', which will be either a ISO 639-1 code or False
      {'language': 'en'}
      {'language': False, 'error': 'Some error', 'scores': {}}

      When return_scores = True;
      {'language': 'en', 'scores': {'en': 0.6, 'es': 0.2}}
    """

    def detect(self, text, clean_text=False, check_confidence=False, min_byte_length=12, min_ngrams=3):

        if clean_text:
            # Removes Urls, emails, alphanumerical & numbers
            text = clean_txt(text)

        min_ngrams = max(1, min_ngrams)
        # Normalize special characters/word separators
        text = re.sub(r'[^\pL]+(?<![\x27\x60\x2019])', ' ', text[:1000], flags=re.UNICODE).strip()
        text = text.lower()
        text = bytes(text, 'utf-8')
        this_length = len(text)

        if this_length > 350:
            # Cut to first whitespace after 350 byte length offset
            text = text[0:min(380, (text.find(b'\x20', 350) or 350))]
        elif this_length < min_byte_length:
            return {'language': False, 'error': 'Text to short', 'scores': {}}

        txt_ngrams = get_byte_ngrams(text)
        num_ngrams = len(txt_ngrams)

        if num_ngrams >= min_ngrams:
            results = calc_scores(txt_ngrams, num_ngrams)

            if self.subset:
                results = LanguageSubset.filter_lang_subset(self, results)

            results.sort(key=lambda x: -x[1])

            if results:
                top_lang = results[0][0]
                # Minimum confidence threshold. 
                if check_confidence:
                    # A minimum of a 24% per ngram score from average
                    next_score = (results[1][0] if len(results) > 1 else 0)
                    if (languageData.avgScore[top_lang] * 0.24 > (results[0][1] / num_ngrams) or 0.01 > abs(
                            results[0][1] - next_score)):
                        return {'language': False,
                                'error': "No language has been identified with sufficient confidence,"
                                         " set checkConfidence to false to avoid this error",
                                'scores': []}
                if not self.return_scores:
                    return {'language': languageData.langCodes[top_lang]}
                else:
                    return {'language': languageData.langCodes[top_lang], 'scores': get_scores(results)}
            return {'language': False, 'error': 'Language not detected', 'scores': {}}
        return {'language': False, 'error': 'Not enough distinct ngrams', 'scores': {}}


def tokenizer(txt):
    return filter(None, re.split(b'\x20', txt))


def clean_txt(txt):
    # Remove URLS
    txt = re.sub(r'[hw]((ttps?://(www\.)?)|ww\.)([^\s/?\.#-]+\.?)+(\/\S*)?', ' ', txt, flags=re.IGNORECASE)
    # Remove emails
    txt = re.sub(r'[a-zA-Z0-9.!$%&?+_`-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9-]{2,64}', ' ', txt)
    # Remove .com domains
    txt = re.sub(r'([A-Za-z0-9-]+\.)+com(\/\S*|[^\pL])', ' ', txt)
    # Remove alphanumerical/number codes
    txt = re.sub(r'[a-zA-Z]*[0-9]+[a-zA-Z0-9]*', ' ', txt)
    return txt


def get_scores(array):
    scores = {}
    for value in array:
        if value[1] == 0:
            break
        scores[languageData.langCodes[value[0]]] = value[1]
    return scores


def calc_scores(txt_ngrams, num_ngrams):
    lang_score = languageData.langScore[:]
    for nbytes, frequency in txt_ngrams.items():
        if nbytes in languageData.ngrams:
            num_langs = len(languageData.ngrams[nbytes])
            # Ngram score multiplier, the fewer languages found the more relevancy. Formula can be fine-tuned.
            if num_langs == 1:
                relevancy = 27
            elif num_langs < 16:
                relevancy = (16 - num_langs) / 2 + 1
            else:
                relevancy = 1

            # Most time-consuming loop, do only the strictly necessary inside
            for lang, ngramFrequency in languageData.ngrams[nbytes].items():
                lang_score[lang] += (ngramFrequency / frequency if frequency > ngramFrequency
                                     else frequency / ngramFrequency) * relevancy + 2
    # This divisor will produce a final score between 0 - ~1, score could be >1. Can be improved.
    result_divisor = num_ngrams * 3.2
    results = []
    for lang in range(len(lang_score)):
        if lang_score[lang]:
            results.append([lang, lang_score[lang] / result_divisor])  # * languageData.scoreNormalizer[lang]
    return results


def get_byte_ngrams(txt):
    tokens = {}
    count_ngrams = 0

    for word in tokenizer(txt):
        length = len(word)

        if length > 70:
            length = 70
        x = 0
        for j in range(0, length - 4, 3):
            this_bytes = (b' ' if j == 0 else b'') + word[j:j + 4]
            tokens[this_bytes] = (1 + tokens[this_bytes] if this_bytes in tokens else 1)
            count_ngrams += 1
            x = 1

        this_bytes = (b' ' if x == 0 else b'') + word[length - 4 if length != 3 else 0:] + b' '
        tokens[this_bytes] = (1 + tokens[this_bytes] if this_bytes in tokens else 1)
        count_ngrams += 1

    # Frequency is multiplied by 15000 at the ngrams database. A reduced number seems to work better.
    # Linear formulas were tried, decreasing the multiplier for fewer ngram strings, no meaningful improvement.
    for nbytes, count in tokens.items():
        tokens[nbytes] = count / count_ngrams * 13200

    return tokens
