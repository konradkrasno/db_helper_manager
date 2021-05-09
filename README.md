# DB helper manager

## Installation

```
python -m venv venv
source venv/bin/activate
pip install db_helper_manager
```

## Configuration
Create setup.ini file in main project directory with following:
```
[db_config]
DIALECT = mysql
NAME = <db_name>
USER = <username>
PASSWORD = <password>
HOST = <host>
PORT = <port>
```

## Usage

```
db_helper_manager update_unit_prices
db_helper_manager fetch_product_data_as_csv
```

## Running tests

```
python -m unittest
```
