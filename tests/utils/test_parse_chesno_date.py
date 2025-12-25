import unittest
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup

from src.utils.parse_chesno_date import parse_chesno_date
from tests.base_test import BaseTestCase


def beautifier(date: str) -> BeautifulSoup:
    tagged_date = f"""<div class="date">{date}</div>"""
    return BeautifulSoup(tagged_date, "html.parser")


class TestParseChesnoDate(BaseTestCase):

    def test_parse_returns_right_date_with_year(self):
        """This test checks whether test_parse_chesno_date return correct dates for
        '11 липня 2024 р. 11:53' examples"""

        result = parse_chesno_date(beautifier('11 липня 2024 р. 11:53'))
        expected = datetime(2024, 7, 11, 11, 53,
                            tzinfo=timezone(timedelta(hours=2)))

        self.assertEqual(result, expected)


    def test_parse_returns_right_date_without_year(self):
        """This test checks whether test_parse_chesno_date return correct dates for
        '21 листопада 10:26' examples"""

        result = parse_chesno_date(beautifier('21 листопада 10:26'))
        expected = datetime(datetime.now().year, 11, 21, 10, 26,
                            tzinfo=timezone(timedelta(hours=2)))

        self.assertEqual(result, expected)

    def test_parse_incorrect_dates(self):
        """This test checks whether test_parse_chesno_date
        returns None for incorrect dates"""

        inputs = [beautifier(input) for input in ['', '21 квартира 23:24', '35 липня 10:24']]

        for input in inputs:
            self.assertEqual(parse_chesno_date(input), None)

if __name__ == '__main__':
    unittest.main()
