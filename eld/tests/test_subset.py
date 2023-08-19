import unittest
import sys
import os

# Make sure, local package is imported instead of pip package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)  # prioritize the local package
# sys.path.append('../..')

from eld import LanguageDetector


# Mostly functional testing, when functions are more mature I will add some more unit tests
class TestDetector(unittest.TestCase):
    def test_load_eld(self):
        detector = LanguageDetector()
        self.assertIsInstance(detector, LanguageDetector)

    def test_dynamic_subset_detect(self):
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.dynamic_lang_subset(lang_subset)
        result = len(detector.detect('How are you? Bien, gracias').scores())
        message = "Expected: 1 score, subset of only one language"
        self.assertEqual(result, 1, message)

    def test_remove_dynamic_subset(self):
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.dynamic_lang_subset(lang_subset)
        detector.dynamic_lang_subset(None)
        result = len(detector.detect('How are you? Bien, gracias').scores())
        self.assertGreater(result, 1)

    def test_subset_detect(self):
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        result = len(detector.detect('How are you? Bien, gracias').scores())
        message = "Expected: 1 score, subset of only one language"
        self.assertEqual(result, 1, message)

    def test_remove_subset(self):
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        detector.lang_subset(None)
        result = len(detector.detect('How are you? Bien, gracias').scores())
        self.assertGreater(result, 1)

    def test_save_subset_file(self):
        # TODO use importlib or pathlib to check subset file as package resource
        file = os.path.dirname(__file__) + '/../resources/ngrams/subset/ngramsM60-1_2rrx014rx6ypsas6tplo1gtcnmiv5mz.py'
        if os.path.exists(file):
            os.remove(file)
        detector = LanguageDetector()
        lang_subset = ['en']
        detector.lang_subset(lang_subset)
        result = os.path.exists(file)
        message = "Subset languages file Not saved: " + file
        self.assertEqual(result, True, message)

    def test_load_ngrams_detect(self):
        detector = LanguageDetector('ngramsM60-6_5ijqhj4oecs310zqtm8u9pgmd9ox2yd')
        result = detector.detect('Hola, cómo te llamas?').language
        self.assertEqual(result, 'es')


if __name__ == '__main__':
    unittest.main(verbosity=2)
