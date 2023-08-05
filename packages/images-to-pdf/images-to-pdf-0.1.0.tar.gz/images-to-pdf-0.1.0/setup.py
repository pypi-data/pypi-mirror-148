#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "Pillow==9.1.0"]

test_requirements = []

setup(
    author="Lucas Paula",
    author_email="luolcami@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Convert all passed images into a single pdf file",
    entry_points={
        "console_scripts": [
            "img2pdf=images_to_pdf.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="images_to_pdf",
    name="images-to-pdf",
    packages=find_packages(include=["images_to_pdf", "images_to_pdf.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/lucas8107/images-to-pdf",
    version="0.1.0",
    zip_safe=False,
)
