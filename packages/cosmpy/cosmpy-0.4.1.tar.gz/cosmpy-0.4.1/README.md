<h1 align="center">
    <b>CosmPy</b>
</h1>

<p align="center">
  <a href="https://pypi.org/project/cosmpy/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/cosmpy">
  </a>
  <a href="https://pypi.org/project/cosmpy/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/cosmpy">
  </a>
  <a>
    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/cosmpy">
  </a>
  <a href="https://github.com/fetchai/cosmpy/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/pypi/l/cosmpy"> 
  </a>
</p>
<p align="center">
  <a href="https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml">
    <img alt="AEA framework sanity checks and tests" src="https://github.com/fetchai/cosmpy/actions/workflows/workflow.yml/badge.svg">
  </a>

[comment]: <> (  <a href="">)
[comment]: <> (    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/fetchai/cosmpy">)
[comment]: <> (  </a>)

  <a href="https://img.shields.io/badge/lint-flake8-blueviolet">
    <img alt="flake8" src="https://img.shields.io/badge/lint-flake8-yellow" >
  </a>
  <a href="https://github.com/python/mypy">
    <img alt="mypy" src="https://img.shields.io/badge/static%20check-mypy-blue">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Black" src="https://img.shields.io/badge/code%20style-black-black">
  </a>
  <a href="https://github.com/PyCQA/bandit">
    <img alt="mypy" src="https://img.shields.io/badge/security-bandit-lightgrey">
  </a>
</p>

<p align="center">
A python library for interacting with cosmos based blockchain networks
</p>

## Installing

To install the project use:

    pip3 install cosmpy

## Getting started

Below is a simple example for querying an account's balance and sending funds from one account to another using `RestClient`:

    from cosmpy.clients.ledger import CosmosLedger
    from cosmpy.clients.crypto import CosmosCrypto, Coin

    # Data
    rest_node_address = "http://the_rest_endpoint"
    alice_crypto = CosmosCrypto(private_key_str="<private_key_in_hex_format>"))
    chain_id = "some_chain_id"
    denom = "some_denomination"
    bob_address = "some_address"

    ledger = CosmosLedger(chain_id=chain_id, rest_node_address=rest_endpoint_addres)
    
    # Query Alice's Balance
    res = ledger.get_balance(alice_crypto.get_address(), denom)
    print(f"Alice's Balance: {res} {denom}")
    
    # Send 1 <denom> from Alice to Bob
    ledger.send_tokens(alice_crypto, bob_address, [Coin(amount="1", denom=denom)])

## Documentation

To see the documentation, first run:

```bash
make generate-docs
```

Then (if on Linux or MacOS):

```bash
make open-docs
```

And if on windows, open `docs/build/html/index.html`.

## Examples

Under the `examples` directory, you can find examples of basic ledger interactions with `cosmpy` using both REST and gRPC, e.g. querying, sending a transaction, interacting with a smart contract, and performing atomic swaps. To run any example `<example_file_name>`:  

  ```bash
  python ./examples/<example_file_name>.py
  ```

## Extra Resources

* [Github Repo](https://github.com/fetchai/cosmpy)
* [Bug Reports](https://github.com/fetchai/cosmpy/issues)
* [Discussions](https://github.com/fetchai/cosmpy/discussions)
