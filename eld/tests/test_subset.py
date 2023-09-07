import pytest
import sys
import os

# Make sure, local package is imported instead of pip package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)  # prioritize the local package
# sys.path.append('../..')

from eld import LanguageDetector


# Mostly functional testing, when functions are more mature I will add some more unit tests

def test_load_eld():
    detector = LanguageDetector()
    assert isinstance(detector, LanguageDetector)


def test_dynamic_subset_detect():
    detector = LanguageDetector()
    lang_subset = ['en']
    detector.dynamic_lang_subset(lang_subset)
    result = len(detector.detect('How are you? Bien, gracias').scores())
    assert result == 1, 'Expected: 1 score, subset of only one language'


def test_remove_dynamic_subset():
    detector = LanguageDetector()
    lang_subset = ['en']
    detector.dynamic_lang_subset(lang_subset)
    detector.dynamic_lang_subset(None)
    result = len(detector.detect('How are you? Bien, gracias').scores())
    assert result > 1


def test_subset_detect():
    detector = LanguageDetector()
    lang_subset = ['en']
    detector.lang_subset(lang_subset)
    result = len(detector.detect('How are you? Bien, gracias').scores())
    assert result == 1, 'Expected: 1 score, subset of only one language'


def test_remove_subset():
    detector = LanguageDetector()
    lang_subset = ['en']
    detector.lang_subset(lang_subset)
    detector.lang_subset(None)
    result = len(detector.detect('How are you? Bien, gracias').scores())
    assert result > 1


def test_save_subset_file():
    # TODO use importlib or pathlib to check subset file as package resource
    file = os.path.dirname(__file__) + '/../resources/ngrams/subset/ngramsM60-1_2rrx014rx6ypsas6tplo1gtcnmiv5mz.py'
    if os.path.exists(file):
        os.remove(file)
    detector = LanguageDetector()
    lang_subset = ['en']
    detector.lang_subset(lang_subset)
    result = os.path.exists(file)
    assert result is True, 'Subset languages file Not saved: ' + file


def test_load_ngrams_detect():
    detector = LanguageDetector('ngramsM60-6_5ijqhj4oecs310zqtm8u9pgmd9ox2yd')
    result = detector.detect('Hola, cómo te llamas?').language
    assert result == 'es'
