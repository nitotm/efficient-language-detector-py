import os
import time
import sys

sys.path.append('..')

from src.languageDetector import LanguageDetector

langDetect = LanguageDetector()
files = ['tweets.txt', 'big-test.txt', 'sentences.txt', 'word-pairs.txt', 'single-words.txt']

for file in files:
    content = open(file, encoding="utf-8").read()
    lines = content.strip().split("\n")
    texts = []

    for line in lines:
        values = line.split("\t")
        texts.append([values[1], values[0]])

    total = len(texts)
    correct = 0
    start = time.time()

    for text in texts:
        if langDetect.detect(text[0], False, False, 0, 1)['language'] == text[1]:
            correct += 1

    time_taken = time.time() - start
    print(f"{file} - Correct ratio: {round((correct / total) * 100, 2)}% Time: {time_taken}\n")

"""
tweets.txt - Correct ratio: 99.28% Time: 0.9556999206542969
big-test.txt - Correct ratio: 99.41% Time: 7.8356194496154785
sentences.txt - Correct ratio: 98.77% Time: 6.7327587604522705
word-pairs.txt - Correct ratio: 87.55% Time: 2.636420488357544
single-words.txt - Correct ratio: 73.31% Time: 2.12335205078125
"""
