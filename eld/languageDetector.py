# Copyright 2023 Nito T.M.
# License https://www.apache.org/licenses/LICENSE-2.0 Apache-2.0
# Author Nito T.M. (https://github.com/nitotm)
# Package pypi.org/project/eld/

import regex as re

from eld.languageData import languageData
from eld.languageSubset import LanguageSubset
from eld.languageResult import LanguageResult


class LanguageDetector(LanguageSubset):
    def __init__(self, subset_file=''):
        super().__init__()
        languageData.load_ngrams(subset_file)
        self.__do_clean_text = False
        self.VERSION = '1.0.6'  # Has to match setup.py version

    def detect(self, text):
        """
        Returns the language detected for a given UTF-8 string, as an ISO 639-1 code
            LanguageResult object { language = 'es', scores() = {'es': 0.5, 'et': 0.2}, is_reliable() = True }

        Args:
            text (str): UTF-8 string

        Returns:
            object LanguageResult: language (str or None), scores() (dict or None), is_reliable() (bool)
        """
        if self.__do_clean_text:
            # Removes Urls, emails, alphanumerical & numbers
            text = get_clean_txt(text)
        text = _normalize_text(text)
        txt_ngrams = _get_byte_ngrams(text)
        num_ngrams = len(txt_ngrams)
        results = _calculate_scores(txt_ngrams, num_ngrams)

        if results:
            if self.subset:
                results = LanguageSubset._filter_lang_subset(self, results)
            results.sort(key=lambda x: -x[1])
            return LanguageResult(results, num_ngrams)
        return LanguageResult()

    def clean_text(self, set_bool):
        self.__do_clean_text = (True if set_bool else False)


def _tokenizer(txt):
    return filter(None, re.split(b'\x20', txt))


def get_clean_txt(txt):
    """Removes parts of a string, that may be considered as "noise" for language detection"""
    # Remove URLS
    txt = re.sub(r'[hw]((ttps?://(www\.)?)|ww\.)([^\s/?\.#-]+\.?)+(\/\S*)?', ' ', txt, flags=re.IGNORECASE)
    # Remove emails
    txt = re.sub(r'[a-zA-Z0-9.!$%&?+_`-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9-]{2,64}', ' ', txt)
    # Remove .com domains
    txt = re.sub(r'([A-Za-z0-9-]+\.)+com(\/\S*|[^\pL])', ' ', txt)
    # Remove alphanumerical/number codes
    txt = re.sub(r'[a-zA-Z]*[0-9]+[a-zA-Z0-9]*', ' ', txt)
    return txt


def _normalize_text(text):
    """Normalize special characters/word separators"""
    text = re.sub(r'[^\pL]+(?<![\x27\x60\x2019])', ' ', text[:1000], flags=re.UNICODE).strip()
    text = text.lower()
    text = bytes(text, 'utf-8')
    this_length = len(text)

    if this_length > 350:
        # Cut to first whitespace after 350 byte length offset
        text = text[0:min(380, (text.find(b'\x20', 350) or 350))]
    return text


def _calculate_scores(txt_ngrams, num_ngrams):
    """Calculate scores for each language from the given Ngrams"""
    lang_score = languageData.lang_score[:]
    for bytes_, frequency in txt_ngrams.items():
        if bytes_ in languageData.ngrams:
            lang_count = len(languageData.ngrams[bytes_])
            # Ngram score multiplier, the fewer languages found the more relevancy. Formula can be fine-tuned.
            if lang_count == 1:
                relevancy = 27
            elif lang_count < 16:
                relevancy = (16 - lang_count) / 2 + 1
            else:
                relevancy = 1

            # Most time-consuming loop, do only the strictly necessary inside
            for lang, global_frequency in languageData.ngrams[bytes_].items():
                lang_score[lang] += (global_frequency / frequency if frequency > global_frequency
                                     else frequency / global_frequency) * relevancy + 2
    # This divisor will produce a final score between 0 - ~1, score could be >1. Can be improved.
    result_divisor = num_ngrams * 3.2
    results = []
    for lang in range(len(lang_score)):
        if lang_score[lang]:
            results.append([lang, lang_score[lang] / result_divisor])  # * languageData.scoreNormalizer[lang]
    return results


def _get_byte_ngrams(txt):
    """Gets Ngrams from a given string"""
    byte_grams = {}
    count_ngrams = 0

    for word in _tokenizer(txt):
        length = len(word)

        if length > 70:
            length = 70
        x = 0
        for j in range(0, length - 4, 3):
            this_bytes = (b' ' if j == 0 else b'') + word[j:j + 4]
            byte_grams[this_bytes] = (1 + byte_grams[this_bytes] if this_bytes in byte_grams else 1)
            count_ngrams += 1
            x = 1

        this_bytes = (b' ' if x == 0 else b'') + word[length - 4 if length != 3 else 0:] + b' '
        byte_grams[this_bytes] = (1 + byte_grams[this_bytes] if this_bytes in byte_grams else 1)
        count_ngrams += 1

    # Frequency is multiplied by 15000 at the ngrams database. A reduced number seems to work better.
    # Linear formulas were tried, decreasing the multiplier for fewer ngram strings, no meaningful improvement.
    for bytes_, count in byte_grams.items():
        byte_grams[bytes_] = count / count_ngrams * 13200

    return byte_grams
