import unittest
import os
import sys

# Make sure, local package is imported instead of pip package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)  # prioritize the local package
# sys.path.append('../..')

from eld import LanguageDetector
from eld.languageDetector import get_clean_txt


# Mostly functional testing, when functions are more mature I will add some more unit tests
class TestDetector(unittest.TestCase):
    def test_print_version(self):
        detector = LanguageDetector()
        print(detector.VERSION)

    def test_load_eld(self):
        detector = LanguageDetector()
        self.assertIsInstance(detector, LanguageDetector)

    def test_simple_detect(self):
        detector = LanguageDetector()
        result = detector.detect('Hola, cómo te llamas?').language
        self.assertEqual(result, 'es')

    def test_get_multiple_scores(self):
        detector = LanguageDetector()
        detector.return_scores = True
        result = len(detector.detect('Hola, cómo te llamas?').scores())
        message = "Expected: >1 scores"
        self.assertGreater(result, 1, message)

    def test_detect_error_empty_text(self):
        detector = LanguageDetector()
        result = detector.detect('').language
        self.assertEqual(result, None)

    def test_clean_text(self):
        text = "https://www.google.com/\n" \
               "mail@gmail.com\n" \
               "google.com/search?q=search&source=hp\n" \
               "12345 A12345\n"
        result = get_clean_txt(text).strip()
        self.assertEqual(result, '')

    def test_check_confidence(self):
        detector = LanguageDetector('ngramsM60')
        text = 'zxz zcz zvz zbz znz zmz zlz zsz zdz zkz zjz pelo'
        result = detector.detect(text).is_reliable()
        self.assertEqual(result, False)

    def test_load_ngrams_detect(self):
        detector = LanguageDetector('ngramsM60-6_5ijqhj4oecs310zqtm8u9pgmd9ox2yd')
        result = detector.detect('Hola, cómo te llamas?').language
        self.assertEqual(result, 'es')

    def test_accuracy_m_bigtest(self):
        # TODO use importlib or pathlib to open txt file as package eld.tests.data resource
        detector = LanguageDetector('ngramsM60')
        file = open('data/big-test.txt', encoding="utf-8")  # '../../benchmark/big-test.txt'
        content = file.read()
        file.close()
        lines = content.strip().split("\n")
        total = 0
        correct = 0
        for line in lines:
            total += 1
            values = line.split("\t")
            if detector.detect(values[1]).language == values[0]:
                correct += 1
        if total < 60000:
            raise self.skipTest("big-test.txt was not load correctly, too few lines")
        result = correct / total * 100
        # a bit of margin, depending on tie scores order, avg. might change a bit
        self.assertGreater(result, 99.4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
