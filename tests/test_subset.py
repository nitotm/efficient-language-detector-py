import unittest
import sys
import os

sys.path.append('..')

from src.eld.languageDetector import LanguageDetector
# from eld import LanguageDetector

# Mostly functional testing, when functions are more mature I will add some more unit tests
class TestDetector(unittest.TestCase):
    def test_load_eld(self):
        detector = LanguageDetector()
        self.assertIsInstance(detector, LanguageDetector)

    def test_dynamic_subset_detect(self):
        detector = LanguageDetector()
        detector.return_scores = True
        lang_subset = ['en']
        detector.dynamic_lang_subset(lang_subset)
        result = len(detector.detect('How are you? Bien, gracias')['scores'])
        message = "Expected: 1 score, subset of only one language"
        self.assertEqual(result, 1, message)

    def test_remove_dynamic_subset(self):
        detector = LanguageDetector()
        detector.return_scores = True
        lang_subset = ['en']
        detector.dynamic_lang_subset(lang_subset)
        detector.dynamic_lang_subset(False)
        result = len(detector.detect('How are you? Bien, gracias')['scores'])
        self.assertGreater(result, 1)

    def test_subset_detect(self):
        detector = LanguageDetector()
        detector.return_scores = True
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        result = len(detector.detect('How are you? Bien, gracias')['scores'])
        message = "Expected: 1 score, subset of only one language"
        self.assertEqual(result, 1, message)

    def test_remove_subset(self):
        detector = LanguageDetector()
        detector.return_scores = True
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        detector.lang_subset(False)
        result = len(detector.detect('How are you? Bien, gracias')['scores'])
        self.assertGreater(result, 1)

    def test_save_subset_file(self):
        file = os.path.dirname(__file__) + '/../src/eld/ngrams/ngrams_17ba0791499db908433b80f37c5fbc89b870084b.py'
        if os.path.exists(file):
            os.remove(file)
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        result = os.path.exists(file)
        message = "Subset languages file Not saved"
        self.assertEqual(result, True, message)

    def test_load_ngrams_detect(self):
        detector = LanguageDetector('ngrams_2f37045c74780aba1d36d6717f3244dc025fb935')
        result = detector.detect('Hola, cómo te llamas?')['language']
        self.assertEqual(result, 'es')


if __name__ == '__main__':
    unittest.main(verbosity=2)
