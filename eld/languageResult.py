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
import json
from .languageData import languageData


class LanguageResult:
    def __init__(self, results=None, num_ngrams=None):
        self.language = (languageData.lang_codes[results[0][0]] if results else None)
        self.__results = results
        self.__num_ngrams = num_ngrams

    def __str__(self):
        return json.dumps({'<object>': {
            'language': self.language,
            'scores()': self.scores(),
            'is_reliable()': self.is_reliable()
        }
        })

    def scores(self):
        return _get_scores(self.__results)

    def is_reliable(self):
        if not self.language or self.__num_ngrams < 3 or not self.__results:
            return False
        next_score = (self.__results[1][1] if len(self.__results) > 1 else 0)
        # A minimum of a 24% from the average score
        if languageData.avg_score[self.language] * 0.24 > (self.__results[0][1] / self.__num_ngrams) \
                or 0.01 > abs(self.__results[0][1] - next_score):
            return False
        return True


def _get_scores(results):
    scores = {}
    if results:
        for value in results:
            scores[languageData.lang_codes[value[0]]] = value[1]
    return scores
