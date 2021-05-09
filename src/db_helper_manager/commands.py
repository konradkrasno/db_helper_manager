import csv
from typing import List

from db_helper_manager.config import logger
from db_helper_manager.rates import Rate
from sqlalchemy import text
from sqlalchemy.orm import Session


class UpdateUnitPrices(Rate):
    """Updates UnitPriceEuro and UnitPriceUSD involving current exchange rate."""

    def update_unit_prices(self) -> None:
        with Session(self.default_db_engine) as session:
            session.execute(
                text(
                    "UPDATE product SET UnitPriceEuro=UnitPrice * :EURORate, UnitPriceUSD=UnitPrice * :USDRate"
                ),
                [
                    {
                        "EURORate": self.get_current_rate_in_pln("eur"),
                        "USDRate": self.get_current_rate_in_pln("usd"),
                    }
                ],
            )
            session.commit()
        logger.info("Prices successfully updated.")


class FetchProductData:
    """
    Fetches all data from the 'product' table from the database
    and saves it to the product.csv file.
    """

    @property
    def fields(self) -> List:
        return [
            "ProductID",
            "DepartmentID",
            "Category",
            "IDSKU",
            "ProductName",
            "Quantity",
            "UnitPrice",
            "UnitPriceUSD",
            "UnitPriceEuro",
            "Ranking",
            "ProductDesc",
            "UnitsInStock",
            "UnitsInOrder",
        ]

    def fetch_product_data_as_csv(self) -> None:
        with Session(self.default_db_engine) as session:
            result = session.execute(
                text("SELECT {} from product".format(" ,".join(self.fields)))
            )
            with open("products.csv", "w", newline="") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerow(self.fields)
                for product in result:
                    writer.writerow(product)
        logger.info("Data successfully downloaded.")


class Commands(UpdateUnitPrices, FetchProductData):
    """Links all commands and handles them. Helps register commands in DBManager class."""

    available_commands = ["update_unit_prices", "fetch_product_data_as_csv"]

    @classmethod
    def print_command_list(cls) -> None:
        print("Available commands:")
        [print(f"  {command}") for command in cls.available_commands]

    def execute_command(self, command: str, *args):
        if command in self.available_commands:
            try:
                self.__getattribute__(command)(*args)
            except TypeError as e:
                print(e.__str__())
            except Exception as e:
                print(e.__str__())
                logger.exception(e)
        else:
            print(f"Command '{command}' not found")
            self.print_command_list()
