import numpy
import pandas as pd
import requests
from bs4 import Tag

from liq_rates import (collect_data_for_df, get_dataframes_from_categories,
                       get_df_with_key_rate, get_meeting_days, get_rates,
                       get_ruonia_df, processing_request, processing_ruonia,
                       update_indicators)

bs_tag = Tag
response_type = requests.models.Response


def test__get_url(link):
    response = requests.get(link)

    assert response.status_code == 200
    assert isinstance(response, response_type)
    assert len(response.text) > 1


def test__collect_data_for_df(link):
    response = requests.get(link).text

    rows = collect_data_for_df(response)

    assert len(rows) > 0
    assert isinstance(rows, list)
    assert len(rows[0]) == 3


def test__get_ruonia_df(date_from, date_to):
    df = get_ruonia_df(date_from, date_to)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (30, 3)
    assert df.columns.tolist() == ['Дата ставки', 'Значение, %', 'Объем сделок RUONIA, млрд руб.']


def test__processing_ruonia(date_from, date_to):
    df = processing_ruonia(date_from, date_to)

    assert isinstance(df, pd.DataFrame)
    assert df['Значение, %'].dtype.type == numpy.float64
    assert df['Дата ставки'].dtype.type == numpy.datetime64


# class TestGetMeetingDays(unittest.TestCase):

#     def get_request_mock(self, mock_request):
#         mock_response = Mock()
#         mock_response.status_code = 200
#         mock_response.text.return_value = 'Hello'
#         mock_request.get.return_value = mock_response
#         return mock_request

#     @patch('liq_rates.requests')
#     def test__get_meeting_days(self, requests):
#         with patch('liq_rates.get_url', new=self.get_request_mock):
#             dates = get_meeting_days()

#             assert dates == []


def test__processing_request(link_key_rate_no_parametres, date_from, date_to):
    response = processing_request(link_key_rate_no_parametres, date_from, date_to)

    assert response.status_code == 200
    assert isinstance(response, response_type)
    assert len(response.text) > 1


def test__get_df_with_key_rate(link_key_rate):
    response = requests.get(link_key_rate)
    df = get_df_with_key_rate(response)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (30, 2)
    assert df.columns.tolist() == ['Дата', 'Ставка']


def test__update_indicators(link_key_rate_no_parametres, date_from, date_to):
    response = processing_request(link_key_rate_no_parametres, date_from, date_to)
    df = get_df_with_key_rate(response)
    df = update_indicators(df)

    assert df.columns.tolist() == ['Дата', 'CBR_key_rate']
    assert df['Дата'].dtype.type == numpy.datetime64
    assert df['CBR_key_rate'].dtype.type == numpy.float64


def test__get_rates(name_file):
    df_roisfix = pd.read_excel(name_file, sheet_name="roisfix")

    rate_1, rate_2, rate_3, rate_4 = get_rates(df_roisfix)

    assert all(isinstance(rates, list) for rates in [rate_1, rate_2, rate_3, rate_4])
    assert all((len(rates) > 0) for rates in [rate_1, rate_2, rate_3, rate_4])


def test__get_dataframes_from_categories(date_from, date_to):
    categories = ["ruonia", "roisfix", "nfeaswap", "rurepo"]

    list_rates = get_dataframes_from_categories(categories, date_from, date_to)

    assert len(list_rates) == 4
    assert isinstance(list_rates, list)
    assert all(isinstance(df, pd.DataFrame) for df in list_rates)
    assert all(df.shape[0] > 0 for df in list_rates)


def test__get_meeting_days(link_key_events):
    response = requests.get(link_key_events)
    meet_dates = get_meeting_days()

    assert response.status_code == 200
    assert isinstance(response, response_type)
    assert len(meet_dates) > 0
    assert isinstance(meet_dates, list)
    assert isinstance(meet_dates[0], bs_tag)
