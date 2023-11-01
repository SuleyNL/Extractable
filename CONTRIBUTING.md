# Contribution Guidelines

👋 Welcome to the Extractable project! We're excited to have you on board. Extractable is an open-source library designed to make table extraction from PDFs using machine learning accessible to everyone. Your contributions are invaluable in helping us achieve this goal.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [Maintainers](#maintainers)
  - [For Testing](#for-testing)
  - [For Publishing](#for-publishing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features
🚀 Here are some of the key features of Extractable:

- **Table Extraction from PDFs**: Extractable utilizes machine learning models to extract tables from PDFs, simplifying data extraction from large datasets.

- **Open-Source and Collaborative**: We believe in community collaboration, and Extractable is an open-source project where your contributions are highly encouraged.

- **PDF Test Table Generator**: We've created a unique dataset to simulate real-world scenarios and evaluate machine learning models. Your input can help us enhance our testing scenarios.

- **Comparative Analyses**: We've conducted thorough comparative analyses of various machine learning models to determine their effectiveness in extracting tables from PDFs. Your insights could add to this valuable resource.

- **Robust Data Pipelines**: Our data pipelines are designed for processing and analyzing large volumes of PDF data while emphasizing code readability and sustainability.

## Installation
🛠️ To get started with Extractable, simply install it using pip:

```bash
pip install Extractable
Extractable is designed for Python 3.10.
```

## Usage
💡 Using Extractable is straightforward. Import the library and use its functions as shown below:

```python
import extractable

input_file = "path_to/your_input.pdf"
output_file = "path_to/your_preferred_output"

# Extract tables from a PDF file
tables = extractable.Extractor.extract(input_file, output_file)

# It's that simple!
```

## Architecture
🏗️ To visualize the internal dependencies of this codebase, we utilize the 'Codesee' extension. With each pull request, a Codesee bot will analyze architecture changes, providing insightful visualizations. Here's a snapshot:

![Code and dependency Architecture of the codebase](Extractable_Architecture_3_10_2023.png)

## Contributing
🤝 Extractable is a community-driven project, and we welcome contributions from all. If you're interested in contributing, please follow our contribution guidelines. Don't hesitate to reach out to us on our GitHub repository if you have any questions or need assistance.

## Maintainers
👩‍💼👨‍💼 Our maintainers oversee the development and management of Extractable. Here are the steps you might need as a maintainer:

### Testing
Before publishing a new version of Extractable, it's crucial to run tests to ensure the code's functionality remains intact. Follow these steps:

Run regression tests using the following command:
```bash
pdm run pytest -k "tests/ and Test_"
```

To test the library's functionality in a real-life scenario without uploading it to the official Pypi.org filesystem, follow these steps:
Build the distribution files:
```bash
pdm build
```

Push the library to the testing environment:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/extractable-[version]* --verbose
```

Install the testing library:
```bash
pip uninstall Extractable
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple Extractable==[version]
```

### Publishing
When it's time to publish a new version of Extractable, follow these steps:

Update the version in `src/version.py` and the `pyproject.toml` file to the new version (old version +1).

Build the distribution files:

```bash
pdm build
```
Push the library to the real Pypi environment:

```bash
twine upload dist/extractable-[version]* --verbose
```
Install the updated library:

```bash
pip uninstall Extractable
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple Extractable==[version]
```

## License
📜 Extractable is free to use. We encourage you to use it as you see fit, but we ask that you respect Microsoft's authorship of the TATR software and provide appropriate attribution when sharing or distributing it. Please note that we offer no warranties or guarantees about the software's functionality, and we are not liable for any damages resulting from its use.

## Acknowledgments
🙏 We'd like to express our gratitude to Microsoft for developing the TATR library and making it open-source. We've built upon their work to create Extractable and are thankful for their contribution to the open-source community. Your contributions can further enhance this collaborative effort.
