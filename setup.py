import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eld",
    version="0.9.1",
    author="Nito T.M.",
    #    author_email = "",
    description="Fast and accurate natural language detection. Detector written in Python. Nito-ELD, ELD.",
    keywords='nlp language natural-language-processing natural-language language-detection language-detector language-identification',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['regex'],
    url="https://github.com/nitotm/efficient-language-detector-py/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    data_files=[('', ['demo.py']),
                ('benchmarks',
                 ['benchmarks/bench.py',
                  'benchmarks/big-test.txt',
                  'benchmarks/sentences.txt',
                  'benchmarks/sentences_avg_py.png',
                  'benchmarks/single-words.txt',
                  'benchmarks/table_accuracy_py.svg',
                  'benchmarks/table_time_py.svg',
                  'benchmarks/tweets.txt',
                  'benchmarks/word-pairs.txt'])],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7"
)
