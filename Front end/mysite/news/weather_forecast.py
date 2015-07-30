__author__ = 'Work'

import forecastio

def weather_forecast(latitude,longtitude):
        api_key = "ffc1b62d11bbb159030f123c4214a6af"
        lat = latitude
        lng = longtitude

        forecast = forecastio.load_forecast(api_key, lat, lng)

        byHour = forecast.hourly()
        hourly = byHour.summary

        byCurrently = forecast.currently()
        current_temp = byCurrently.temperature
        current_summary = byCurrently.summary

        hourly_data = []

        for hourlyData in byHour.data:
                hourly_data.append(hourlyData.temperature)

        forecast = {"hourly": hourly, "current_temp" : current_temp, "current_summary" : current_summary, "hourly_data" : hourly_data}

        return forecast