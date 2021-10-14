from typing import List
from unittest.mock import patch, MagicMock

from src.main import WeatherAPI


def test_fill_up_city_choices() -> None:
    cities: List = [
        {'title': 'London', 'woeid': 123},
        {'title': 'Barcelona', 'woeid': 124},
    ]

    weather_api = WeatherAPI(city_title='lon')
    weather_api.fill_up_city_choices(cities=cities)
    assert weather_api.CITY_CHOICES == [
        {
            'type': 'list',
            'message': 'Select cities',
            'name': 'city_title',
            'choices': [{'name': 'London, 123'}, {'name': 'Barcelona, 124'}],
        }
    ]


def test_check_for_rain_with_clear_weather() -> None:
    forecast_data: List = [{
        'weather_state_abbr': 'c',
        'predictability': '75'
    }]
    with patch.multiple(
        target='src.main.WeatherAPI',
        get_tomorrows_date=MagicMock(return_value='2021/10/14'),
        get_forecast_data=MagicMock(return_value=forecast_data),
    ) as _:
        weather_api = WeatherAPI(city_title='Istanbul')
        weather_api.chosen_city = 'Istanbul'
        rain_state: str = weather_api.check_for_rain('123')
        assert rain_state == 'It won\'t rain tomorrow in Istanbul.'


def test_check_for_rain_with_rainy_weather() -> None:
    forecast_data: List = [{
        'weather_state_abbr': 'hr',
        'predictability': '75'
    }]
    with patch.multiple(
        target='src.main.WeatherAPI',
        get_tomorrows_date=MagicMock(return_value='2021/10/14'),
        get_forecast_data=MagicMock(return_value=forecast_data),
    ) as _:
        weather_api = WeatherAPI(city_title='Istanbul')
        weather_api.chosen_city = 'Istanbul'
        rain_state: str = weather_api.check_for_rain('123')
        assert rain_state == 'It will rain tomorrow in Istanbul, 75% chance.'
