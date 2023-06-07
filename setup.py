from setuptools import setup

import src.version as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Extractable',
    version= version.__version__,
    description='Extract tables from PDFs',
    packages=['Extractable', 'TableGenerator', 'fpdf', 'genalog'],
    #py_modules=['Extractable/Extractor', 'Extractable/library', 'TableGenerator/CreatePDFTable', 'TableGenerator/Options'],
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'sample': ['package_data.dat'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    install_requires=[
        "setuptools >=61.0",
        "toolz ~= 0.12.0",
        "torch ~= 2.0.1",
        "Pillow ~= 9.5.0",
        "transformers ~= 4.29.2",
        "matplotlib >=3",
        "pdf2image ~= 1.16.3",
        "pdf2jpg ~= 1.1",
        "scipy ~= 1.10.1",
        "timm",
        "defusedxml",
        "Faker ~= 18.9.0",
        "build",
        "wheel",
        "mkdocs",
        "pytesseract",
        "PyPDF2",
        "svgwrite",
    ],
    url="https://github.com/SuleyNL/Extractable",
    author="Suleymen C. Kandrouch",
    author_email="suleyleeuw@gmail.com",
)
