import unittest
from typing import Dict
from unittest import TestCase
from unittest.mock import patch, call

from db_helper_manager.db_manager import DBManager
from db_helper_manager.exceptions import ApiError
from db_helper_manager.rates import Rate


class Fixture(TestCase):
    @staticmethod
    def db_config() -> Dict:
        return {
            "DIALECT": "mysql",
            "NAME": "test",
            "USER": "test",
            "PASSWORD": "test",
            "HOST": "localhost",
            "PORT": 3306,
        }

    @staticmethod
    def json() -> Dict:
        return {
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "087/A/NBP/2021",
                    "effectiveDate": "2021-05-07",
                    "mid": 3.7861,
                }
            ],
        }

    def setUp(self) -> None:
        self.manager = DBManager(self.db_config())

    def tearDown(self) -> None:
        pass


class RateTests(Fixture):
    @patch("requests.get")
    def test_get_current_rate_in_pln_when_ok(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = self.json
        rate = Rate.get_current_rate_in_pln("usd")
        self.assertEqual(rate, 3.7861)

    @patch("requests.get")
    def test_get_current_rate_in_pln_when_error(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(ApiError):
            Rate.get_current_rate_in_pln("usd")


class CommandsTests(Fixture):
    @patch("db_helper_manager.commands.logger")
    @patch("db_helper_manager.commands.text")
    @patch("db_helper_manager.commands.UpdateUnitPrices.get_current_rate_in_pln")
    @patch("db_helper_manager.commands.Session.execute")
    def test_update_unit_prices(self, mock_session, mock_rate, mock_text, mock_logger):
        mock_text.return_value = "mocked statement"
        mock_rate.return_value = 3.7861
        self.manager.update_unit_prices()
        mock_session.assert_called_once_with(
            "mocked statement",
            [
                {
                    "EURORate": 3.7861,
                    "USDRate": 3.7861,
                }
            ],
        )
        mock_logger.info.assert_called()

    @patch("db_helper_manager.commands.logger")
    @patch("db_helper_manager.commands.csv.writer")
    @patch("builtins.open")
    @patch("db_helper_manager.commands.Session.execute")
    def test_fetch_product_data_as_csv(
        self, mock_session, mock_open, mock_writer, mock_logger
    ):
        mock_session.return_value = [["fake1"], ["fake2"]]
        self.manager.fetch_product_data_as_csv()
        mock_open.assert_called_once_with("products.csv", "w", newline="")
        expected_calls = [call(self.manager.fields), call(["fake1"]), call(["fake2"])]
        mock_writer().writerow.assert_has_calls(expected_calls)
        mock_logger.info.assert_called_once_with("Data successfully downloaded.")

    @patch("db_helper_manager.commands.UpdateUnitPrices.update_unit_prices")
    @patch("db_helper_manager.commands.FetchProductData.fetch_product_data_as_csv")
    def test_execute_command(self, mock_fetch_data, mock_update_prices):
        self.manager.execute_command("fetch_product_data_as_csv")
        mock_fetch_data.assert_called_once()
        self.manager.execute_command("update_unit_prices")
        mock_update_prices.assert_called_once()

    @patch("db_helper_manager.commands.Commands.print_command_list")
    def test_execute_command_when_wrong_command(self, mock_print_command_list):
        self.manager.execute_command("wrong_command")
        mock_print_command_list.assert_called_once()

    @patch("builtins.print")
    def test_execute_command_when_wrong_args(self, mock_print):
        self.manager.execute_command("update_unit_prices", "arg1", "arg2")
        mock_print.assert_called_once_with(
            "update_unit_prices() takes 1 positional argument but 3 were given"
        )

    @patch("db_helper_manager.commands.logger")
    @patch("db_helper_manager.commands.UpdateUnitPrices.update_unit_prices")
    def test_execute_command_when_error(self, mock_update_prices, mock_logger):
        mock_update_prices.side_effect = Exception("Exception occurred")
        self.manager.execute_command("update_unit_prices")
        mock_logger.exception.assert_called_once_with(mock_update_prices.side_effect)


if __name__ == "__main__":
    unittest.main()
