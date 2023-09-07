import pytest
import os
import sys

# Make sure, local package is imported instead of pip package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)  # prioritize the local package
# sys.path.append('../..')

from eld import LanguageDetector
from eld.languageDetector import get_clean_txt


# Mostly functional testing, when functions are more mature I will add some more unit tests

def test_print_version():
    detector = LanguageDetector()
    print('ELD ver. ' + detector.VERSION)
    assert True


def test_load_eld():
    detector = LanguageDetector()
    assert isinstance(detector, LanguageDetector)


def test_simple_detect():
    detector = LanguageDetector()
    result = detector.detect('Hola, cómo te llamas?').language
    assert result == 'es'


def test_get_multiple_scores():
    detector = LanguageDetector()
    detector.return_scores = True
    result = len(detector.detect('Hola, cómo te llamas?').scores())
    assert result > 1, 'Expected: >1 scores'


def test_detect_error_empty_text():
    detector = LanguageDetector()
    result = detector.detect('').language
    assert result is None


def test_clean_text():
    text = 'https://www.google.com/\n' \
           'mail@gmail.com\n' \
           'oogle.com/search?q=search&source=hp\n' \
           '12345 A12345\n'
    result = get_clean_txt(text).strip()
    assert result == ''


def test_check_confidence():
    detector = LanguageDetector('ngramsM60')
    text = 'zxz zcz zvz zbz znz zmz zlz zsz zdz zkz zjz pelo'
    result = detector.detect(text).is_reliable()
    assert result is False


def test_load_ngrams_detect():
    detector = LanguageDetector('ngramsM60-6_5ijqhj4oecs310zqtm8u9pgmd9ox2yd')
    result = detector.detect('Hola, cómo te llamas?').language
    assert result == 'es'


def test_accuracy_m_bigtest():
    # TODO use importlib or pathlib to open txt file as package eld.tests.data resource
    detector = LanguageDetector('ngramsM60')
    file = open('data/big-test.txt', encoding='utf-8')  # '../../benchmark/big-test.txt'
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
        pytest.fail('big-test.txt was not load correctly, too few lines')
    result = correct / total * 100
    # a bit of margin, depending on tie scores order, avg. might change a bit
    assert result > 99.4

# python -m pytest -v -s test_detector.py
# if __name__ == '__main__':
#    pytest.main(["-v", "test_detector.py"])  # Gives errors
