import requests

from db_helper_manager.exceptions import ApiError


class Rate:
    """Provides rates for specified currency."""

    @staticmethod
    def get_rate_in_pln_url(currency_code: str) -> str:
        return f"http://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/"

    @classmethod
    def get_current_rate_in_pln(cls, currency_code: str) -> str:
        url = cls.get_rate_in_pln_url(currency_code)
        r = requests.get(url)
        if r.status_code != 200:
            raise ApiError(
                "Data has not been retrieved. Status code: '{}'".format(r.status_code)
            )
        return r.json().get("rates")[0].get("mid")
