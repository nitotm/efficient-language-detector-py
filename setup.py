import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eld",
    version="1.0.3",  # Update VERSION at languageDetector.py too
    author="Nito T.M.",
    # author_email = "",
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
    # package_dir={'': 'eld'},
    # packages=setuptools.find_packages(where='eld'),
    packages=['eld', 'eld.tests', 'eld.resources', 'eld.resources.ngrams', 'eld.resources.ngrams.subset'],
	 package_data={'eld.tests': ['data/*.txt']},
    python_requires=">=3.7"
)
