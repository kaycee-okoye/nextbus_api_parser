# NextBus API Python Parser

This Python project provides a simple and efficient way to interact with the NextBus API, which offers information on bus agencies, bus routes, bus stops, bus paths, and bus predictions in the United States. The repository includes four essential files:

1. `api_handler.py`: This module acts as a controller for making API calls to the NextBus API. It also handles the parsing of API responses into appropriate model classes.

2. `data_classes.py`: This file contains the model data classes used to represent and handle data parsed from the NextBus API. These classes help structure the data for easier manipulation and usage within your applications.

3. `xml_handler.py`: The XML handler module includes classes that inherit from `xml.sax.ContentHandler`. These classes are responsible for parsing XML feeds from the NextBus API and transforming the data into the corresponding model classes.

4. `main.py`: The main module implements a command-line interface (CLI) for requesting and displaying bus predictions for a selected bus stop along a selected route within a chosen bus agency. This module serves as a practical example of how to use the other components to interact with the NextBus API.

API documentation: https://retro.umoiq.com/xmlFeedDocs/NextBusXMLFeed.pdf

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/nextbus-api-parser.git
   cd nextbus-api-parser
   ```

2. You can now use the provided command-line interface (CLI) to interact with the NextBus API and retrieve bus predictions.

## Usage

The `main.py` script provides a user-friendly CLI for interacting with the NextBus API. Here's how to use it:

```bash
python main.py
```

Follow the prompts to select a bus agency, route, and bus stop. The script will then fetch and display bus predictions for the chosen stop along the selected route.

## Example

```bash
python main.py
```

```
Welcome to the NextBus API Python Parser CLI!

Please select a bus agency:
1. Agency A
2. Agency B
3. Agency C
...

Enter your choice (1-10): 2

Please select a bus route:
1. Route X
2. Route Y
3. Route Z
...

Enter your choice (1-5): 1

Please select a bus stop:
1. Stop 1
2. Stop 2
3. Stop 3
...

Enter your choice (1-20): 3

Bus predictions for Route Y - Stop 3 (Agency B):

1. Prediction 1: Next bus in 5 minutes
2. Prediction 2: Next bus in 12 minutes
3. Prediction 3: Next bus in 20 minutes
...

Thank you for using the NextBus API Python Parser CLI!
```

# Contributions Guidelines

Please read CONTRIBUTING.md for details on the author's code of conduct, and contribution guidelines.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Special thanks to the NextBus API team for providing access to real-time bus information, making public transportation more accessible to everyone.

Happy coding!
