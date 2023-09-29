import unittest
import requests
from datetime import datetime
from unittest.mock import patch
from fixerio.fixerio_client import FixerioClient, FixerioException


class FixerioHistoricalRatesTestCase(unittest.TestCase):

    def setUp(self):
        self.access_key = 'your-access-key'
        self.date_as_str = "2006-12-24"
        self.date_as_date = datetime.strptime(self.date_as_str, "%Y-%m-%d").date()
        self.client = FixerioClient(self.access_key)
        self.expected_url = f"http://data.fixer.io/api/{self.date_as_str}"

    @patch('requests.get')
    def test_historical_rates_url_with_date(self, mock_requests_get):
        expected_payload = {
            "access_key": self.access_key
        }

        self.client._historical_rates(self.date_as_date)

        mock_requests_get.assert_called_with(self.expected_url, params=expected_payload)

    @patch('requests.get')
    def test_historical_rates_url_with_date_string(self, mock_requests_get):
        expected_payload = {
            "access_key": self.access_key
        }

        self.client._historical_rates(self.date_as_str)

        mock_requests_get.assert_called_with(self.expected_url, params=expected_payload)

    @patch("requests.get")
    def test_request_error_raises_fixer_exception(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("Request failed")

        with self.assertRaises(FixerioException):
            self.client._historical_rates(self.date_as_date)

    @patch("requests.get")
    def test_symbol_in_payload(self, mock_requests_get):
        symbols = ["USD", "EUR"]

        expected_payload = {
            "access_key": self.access_key,
            "symbols": ",".join(symbols)
        }

        self.client._historical_rates(self.date_as_date, symbols=symbols)

        mock_requests_get.assert_called_with(self.expected_url, params=expected_payload)

    @patch("requests.get")
    def test_base_in_payload(self, mock_requests_get):
        base = "GBP"

        expected_payload = {
            "access_key": self.access_key,
            "base": base
        }

        self.client._historical_rates(self.date_as_date, base=base)

        mock_requests_get.assert_called_with(self.expected_url, params=expected_payload)

    @patch("requests.get")
    def test_symbols_and_base_in_payload(self, mock_requests_get):
        symbols = ["USD", "EUR"]
        base = "GBP"

        expected_payload = {
            "access_key": self.access_key,
            "symbols": ",".join(symbols),
            "base": base
        }

        self.client._historical_rates(self.date_as_str, symbols=symbols, base=base)

        mock_requests_get.assert_called_with(self.expected_url, params=expected_payload)
