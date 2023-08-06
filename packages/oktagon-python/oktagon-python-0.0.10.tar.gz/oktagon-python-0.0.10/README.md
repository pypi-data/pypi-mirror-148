# oktagon-python package

[![PyPI](https://img.shields.io/pypi/v/oktagon-python?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/oktagon-python/)

This python package is a tiny utility for verifying & decoding OKTA tokens in python backend services.

For more details please see following [guide](https://github.com/madedotcom/oktagon/docs/oktagon_integration.md)

# Installation

    pip install oktagon-python


## Contributing

    git clone https://github.com/madedotcom/oktagon-python.git
    cd oktagon-python
    make install
    make tests

This will install all the dependencies (including dev ones) and run the tests.

### Pre-commit

We have a configuration for [pre-commit](https://github.com/pre-commit/pre-commit), to add the hook run the following command:

    pre-commit install
