import pytest


@pytest.fixture
def date_from():
    return '01.06.2024'


@pytest.fixture
def date_to():
    return '15.07.2024'


@pytest.fixture
def link(date_from, date_to):
    link = (
        f"https://cbr.ru/hd_base/ruonia/dynamics/"
        f"?UniDbQuery.Posted=True&UniDbQuery.From={date_from}&"
        f"UniDbQuery.To={date_to}"
    )
    return link


@pytest.fixture
def link_key_rate(date_from, date_to):
    url = "https://www.cbr.ru/hd_base/KeyRate/"
    key_url = f"{url}?UniDbQuery.Posted=True&UniDbQuery.From={date_from}&UniDbQuery.To={date_to}"
    return key_url


@pytest.fixture
def link_key_rate_no_parametres():
    return "https://www.cbr.ru/hd_base/KeyRate/"


@pytest.fixture
def link_key_events():
    return "https://www.cbr.ru/dkp/cal_mp/#t11"


@pytest.fixture
def name_file():
    return "LIQ_Rates_Output.xlsx"
