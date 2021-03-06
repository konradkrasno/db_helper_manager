# DB helper manager

## Installation

```
git clone https://github.com/konradkrasno/db_helper_manager.git
cd db_helper_manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m build
pip install dist/db_helper_manager_konradkrasno-0.0.1-py3-none-any.whl
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
python3 -m unittest
```
