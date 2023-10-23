from setuptools import setup, find_packages

import src.version as version

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Extractable',
    version=version.__version__,
    description='Extract tables from PDFs',
    #packages=['Extractable', 'TableGenerator', 'fpdf', 'genalog'],
    #py_modules=['Extractable/Extractor', 'Extractable/library', 'TableGenerator/CreatePDFTable', 'TableGenerator/Options'],
    package_dir={'': 'src'},
    packages=find_packages("src", exclude=['extractable/Tesseract-OCR']),
    include_package_data=True,
    package_data={
        'sample': ['package_data.dat'],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ],
    extras_require={
        "dev": [
            "pytest>=7.3.1",
        ],
    },
    install_requires=[
        "setuptools >=61.0",
        "toolz ~= 0.12.0",
        "torch ~= 2.0.1",
        "Pillow >= 9.2.0",
        "transformers ~= 4.29.2",
        "matplotlib >=3",
        "pdf2image ~= 1.15.1",
        "pdf2jpg ~= 1.1",
        "scipy ~= 1.10.1",
        "timm ~= 0.9.2",
        "defusedxml ~= 0.7.1",
        "Faker ~= 18.9.0",
        "build ~= 0.10.0",
        "wheel ~= 0.40.0",
        "mkdocs ~= 1.4.3",
        "pytesseract >= 0.2.2",
        "PyPDF2 ~= 3.0.1",
        "svgwrite ~= 1.4.3",
        "pandas ~= 2.0.2",
        "pandas-stubs ~= 2.0.2.230605 ",
        "openpyxl ~= 3.1.2",
        "pdm ~= 2.7.0"
    ],
    url="https://github.com/SuleyNL/Extractable",
    author="Suleymen C. Kandrouch",
    author_email="suleyleeuw@gmail.com",
)
