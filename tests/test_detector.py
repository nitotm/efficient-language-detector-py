import unittest
import sys

sys.path.append('..')

from src.eld.languageDetector import *
# from eld import LanguageDetector

# Mostly functional testing, when functions are more mature I will add some more unit tests
class TestDetector(unittest.TestCase):
    def test_load_eld(self):
        detector = LanguageDetector()
        self.assertIsInstance(detector, LanguageDetector)

    def test_simple_detect(self):
        detector = LanguageDetector()
        result = detector.detect('Hola, cómo te llamas?')['language']
        self.assertEqual(result, 'es')

    def test_get_multiple_scores(self):
        detector = LanguageDetector()
        detector.return_scores = True
        result = len(detector.detect('Hola, cómo te llamas?')['scores'])
        message = "Expected: >1 scores"
        self.assertGreater(result, 1, message)

    def test_detect_disable_minimum_length(self):
        detector = LanguageDetector()
        result = detector.detect('To', False, False, 0, 1)['language']
        self.assertEqual(result, 'en', 'Minimum length not properly disabled')

    def test_detect_error_minimum_length(self):
        detector = LanguageDetector()
        result = detector.detect('To')['language']
        self.assertEqual(result, False)

    def test_clean_text(self):
        text = "https://www.google.com/\n" \
               "mail@gmail.com\n" \
               "google.com/search?q=search&source=hp\n" \
               "12345 A12345\n"
        result = clean_txt(text).strip()
        self.assertEqual(result, '')

    def test_check_confidence(self):
        detector = LanguageDetector('ngrams_m')
        text = 'zxz zcz zvz zbz znz zmz zlz zsz zdz zkz zjz pelo'
        result = detector.detect(text=text, clean_text=False, check_confidence=True, min_byte_length=0, min_ngrams=1)[
            'language']
        self.assertEqual(result, False)

    def test_load_ngrams_detect(self):
        detector = LanguageDetector('ngrams_2f37045c74780aba1d36d6717f3244dc025fb935')
        result = detector.detect('Hola, cómo te llamas?')['language']
        self.assertEqual(result, 'es')

    def test_accuracy_m_bigtest(self):
        detector = LanguageDetector('ngrams_m')
        file = open('../benchmarks/big-test.txt', encoding="utf-8")
        content = file.read()
        file.close()
        lines = content.strip().split("\n")
        total = 0
        correct = 0
        for line in lines:
            total += 1
            values = line.split("\t")
            if detector.detect(values[1], False, False, 0, 1)['language'] == values[0]:
                correct += 1
        if total < 60000:
            raise self.skipTest("big-test.txt was not load correctly, too few lines")
        result = correct / total * 100
        # a bit of margin, depending on tie scores order, avg. might change a bit
        self.assertGreater(result, 99.4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
