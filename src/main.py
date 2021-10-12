from datetime import datetime, timedelta
from typing import Tuple, List, Dict

import requests
from PyInquirer import prompt


class WeatherAPI:
    URL: str = 'https://www.metaweather.com/api/location/'
    RAIN_STATES: Tuple = ('lr', 'hr', 's', 'sl')
    QUESTIONS: List = [
        {
            'type': 'input',
            'name': 'city_title',
            'message': 'Type your city title here:',
        }
    ]
    CITY_CHOICES: List = [
        {
            'type': 'list',
            'message': 'Select cities',
            'name': 'city_title',
            'choices': [],
        }
    ]

    def __init__(self, city_title: str) -> None:
        self.city_title: str = city_title
        self.chosen_city: str = ''

    def get_city_data_by_title(self, title) -> List:
        response = requests.get(
            f'{self.URL}search/', params={'query': title}
        )
        response.raise_for_status()
        return response.json()

    def validate_city_data(self, data) -> bool:
        if len(data) == 0:
            return False
        self.fill_up_city_choices(data)
        return True

    def fill_up_city_choices(self, cities):
        for city in cities:
            self.CITY_CHOICES[0]['choices'].append({
                'name': city['title'] + ', ' + str(city['woeid'])
            })

    def get_forecast_data(self, woeid: int, date: str) -> Dict:
        response = requests.get(f'{self.URL}{woeid}/{date}/')
        response.raise_for_status()
        return response.json()[0]

    def get_tomorrows_date(self):
        return (datetime.today() + timedelta(days=1)).strftime('%Y/%m/%d')

    def check_for_rain(self, woeid) -> str:
        date: str = self.get_tomorrows_date()
        data = self.get_forecast_data(woeid, date)
        message: str = f'It won\'t rain tomorrow in {self.chosen_city}.'
        if data['weather_state_abbr'] in self.RAIN_STATES:
            message: str = f'It will rain tomorrow in {self.chosen_city},' \
                           f' {data["predictability"]}% chance.'
        return message


if __name__ == '__main__':
    answer = prompt(WeatherAPI.QUESTIONS)
    weather = WeatherAPI(answer['city_title'])
    city_data = weather.get_city_data_by_title(answer['city_title'])
    if not weather.validate_city_data(city_data):
        print('Could not find such city, please try another one')
    else:
        answer = prompt(weather.CITY_CHOICES)
        woeid = answer['city_title'].split(', ')[1]
        weather.chosen_city = answer['city_title'].split(', ')[0]
        print(weather.check_for_rain(woeid))
