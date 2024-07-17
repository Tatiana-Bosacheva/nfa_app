import numpy
import pandas as pd
import requests
from bs4 import BeautifulSoup

from liq_rates import (get_dataframes_from_categories, get_meeting_days,
                       get_ruonia_rates, processing_request, processing_ruonia,
                       update_indicators)


def test__get_ruonia_rates():
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'
    link = (
        f"https://cbr.ru/hd_base/ruonia/dynamics/"
        f"?UniDbQuery.Posted=True&"
        f"UniDbQuery.From={dt_min}&UniDbQuery.To={stop_date}"
    )

    response = requests.get(link)
    df = get_ruonia_rates(dt_min, stop_date)

    assert response.status_code == 200
    assert isinstance(df, pd.core.frame.DataFrame)
    assert df.shape == (30, 3)
    assert df.columns.tolist() == ['Дата ставки', 'Значение, %', 'Объем сделок RUONIA, млрд руб.']


def test__processing_ruonia():
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'

    df = processing_ruonia(dt_min, stop_date)

    assert df['Значение, %'].dtype.type == numpy.float64
    assert df['Дата ставки'].dtype.type == numpy.datetime64


def test__processing_request():
    url = "https://www.cbr.ru/hd_base/KeyRate/"
    dt_min = '01.06.2024'
    stop_date = '15.07.2024'
    params = {
        "UniDbQuery.Posted": True,
        "UniDbQuery.From": dt_min,
        "UniDbQuery.To": stop_date,
    }

    response = requests.get(url, params=params)
    df = processing_request(url, dt_min, stop_date)

    assert response.status_code == 200
    assert df.shape == (30, 2)
    assert df.columns.tolist() == ['Дата', 'Ставка']


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
    assert isinstance(meet_dates[0], pd.Timestamp)
