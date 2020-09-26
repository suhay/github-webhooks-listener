from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="github-webhooks-listener",
    version="0.2.0",
    author="Matt Suhay",
    author_email="matt@suhay.dev",
    description="A simple listener that will trigger custom scripts when it receives events from GitHub.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = "MIT",
    url="https://github.com/suhay/github-webhooks-listener",
    packages=find_packages(),
    keywords = "github webhooks",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'quart',
        'python-dotenv'
    ],
    python_requires='>=3.8',
)