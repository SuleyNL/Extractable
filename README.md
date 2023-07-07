# Extractable: Table Extraction from PDFs using Machine Learning

Extractable is an open-source library designed to bring the power of state-of-the-art machine learning to everyone. Our goal is to make it easy for anyone to extract tables from PDFs, regardless of their technical expertise. Extractable is built on top of Microsoft's Open Source Table Transformer (TATR) library, which we have expanded to include a variety of new features and improvements.

## Features

Extractable is designed to be easy to use and highly flexible. Some of its key features include:

- **Table Extraction from PDFs**: Extractable uses machine learning models to extract tables from PDFs, enabling users to easily extract data from large datasets.

- **Open-Source and Collaborative**: Extractable is an open-source library designed for easy collaboration and contributions from the community.

- **PDF Test Table Generator**: We have developed a unique dataset to simulate real-world scenarios and benchmark machine learning models, identify the challenges and improve on specific areas. 

- **Comparative Analyses**: We have conducted extensive comparative analyses of various machine learning models to determine their effectiveness in extracting tables from PDFs.

- **Robust Data Pipelines**: We have designed and implemented robust data pipelines for processing and analyzing large volumes of PDF data, with a focus on code-readability and sustainability.

## Installation

To install Extractable, simply use pip:
```pip install Extractable```

Extractable is designed to be used with Python 3.10.

## Usage

To use Extractable, simply import the library and use its functions. We provide comprehensive documentation to get started with the library.

```python
import Extractable

input_file = "path_to/your_input.pdf"
output_file = "path_to/your_preferred_output"

# Extract tables from a PDF file
tables = Extractable.Extractor.extract(input_file, output_file)

# That's how simple it is!
```

## Contributing
Extractable is an open-source project and we welcome contributions from the community. If you would like to contribute, please take a look at our contribution guidelines and feel free to reach out to us on our GitHub repository.

## License
This software is free to use, and I encourage anyone who finds it useful to use it in any way they see fit. While I have not applied any license to the software, I do ask that users respect Microsofts' authorship of the TATR software and give appropriate attribution when sharing or distributing it. Please note that I make no warranties or guarantees about the software's functionality, and I am not liable for any damages resulting from its use

## Acknowledgments
We would like to thank Microsoft for developing the TATR library and making it open-source. We have built upon their work to create Extractable, and we are grateful for their contribution to the open-source community.

