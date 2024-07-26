import unittest
from unittest.mock import Mock, patch

import numpy
import pandas as pd
import requests
from bs4 import BeautifulSoup, Tag

from liq_rates import (get_dataframes_from_categories, get_meeting_days,
                       get_ruonia_df, processing_request, processing_ruonia,
                       update_indicators)

bs_tag = Tag


def test__get_ruonia():
    link = "https://cbr.ru/hd_base/ruonia/dynamics/" \
           "?UniDbQuery.Posted=True&UniDbQuery.From=01.06.2024&" \
           "UniDbQuery.To=15.07.2024"

    response = requests.get(link)

    assert response.status_code == 200
    assert isinstance(response.text, str)
    assert len(response.text) > 1


def test__get_ruonia_df():
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'

    df = get_ruonia_df(dt_min, stop_date)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (30, 3)
    assert df.columns.tolist() == ['Дата ставки', 'Значение, %', 'Объем сделок RUONIA, млрд руб.']


def test__processing_ruonia():
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'

    df = processing_ruonia(dt_min, stop_date)

    assert df['Значение, %'].dtype.type == numpy.float64
    assert df['Дата ставки'].dtype.type == numpy.datetime64


class TestGetMeetingDays(unittest.TestCase):

    def get_request_mock(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text.return_value = 'Hello'
        mock_request.get.return_value = mock_response
        return mock_request

    @patch('liq_rates.requests')
    def test__get_meeting_days(self, requests):
        with patch('liq_rates.get_url', new=self.get_request_mock):
            dates = get_meeting_days()

            assert dates == []


# def test__processing_request():
#     url = "https://www.cbr.ru/hd_base/KeyRate/"
#     dt_min = '01.06.2024'
#     stop_date = '15.07.2024'
#     params = {
#         "UniDbQuery.Posted": True,
#         "UniDbQuery.From": dt_min,
#         "UniDbQuery.To": stop_date,
#     }

#     response = requests.get(url, params=params)
#     df = processing_request(url, dt_min, stop_date)

#     assert response.status_code == 200
#     assert df.shape == (30, 2)
#     assert df.columns.tolist() == ['Дата', 'Ставка']


def test__update_indicators():
    url = "https://www.cbr.ru/hd_base/KeyRate/"
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'

    df = processing_request(url, dt_min, stop_date)
    df = update_indicators(df)

    assert df.columns.tolist() == ['Дата', 'CBR_key_rate']
    assert df['Дата'].dtype.type == numpy.datetime64
    assert df['CBR_key_rate'].dtype.type == numpy.float64


def test__get_dataframes_from_categories():
    categories = ["ruonia", "roisfix", "nfeaswap", "rurepo"]
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'

    list_rates = get_dataframes_from_categories(categories, dt_min, stop_date)

    assert len(list_rates) == 4
    assert all(isinstance(df, pd.DataFrame) for df in list_rates)


def test__get_meeting_days():
    url = "https://www.cbr.ru/dkp/cal_mp/#t11"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dates = soup.find_all("div", class_="main-events_day")
    meet_dates = get_meeting_days()

    assert response.status_code == 200
    assert len(dates) > 0
    assert isinstance(meet_dates, list)
    assert isinstance(meet_dates[0], bs_tag)
