# Third party imports
from setuptools import setup

# This call to setup() does all the work
setup(
    name="mdmls",
    version="0.1.0",
    description="Summarize long document in multiple languages",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/airklizz/mdmls",
    author="Rémi Calizzano",
    author_email="remi.calizzano@gmail.com",
    license="MIT",
    install_requires=[
        "bert-extractive-summarizer>=0.9.0",
        "bert-score>=0.3.11",
        "clean-text>=0.5.0",
        "datasets>=2.1.0",
        "nltk>=3.5",
        "torch>=1.11.0",
        "transformers>=4.18.0",
        "typer>=0.4.0",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["mdmls"],
)