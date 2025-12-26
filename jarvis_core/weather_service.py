import logging

import requests

from .config import OPENWEATHER_API_KEY, LAT, LON


def get_weather_report():
    """
    Lấy thông tin thời tiết hiện tại tại Đồng Nai.
    Return: String mô tả ngắn gọn hoặc thông báo lỗi.
    """
    if not OPENWEATHER_API_KEY:
        return "Weather Data: N/A (Missing API Key)"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=vi"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200:
            desc = data['weather'][0]['description']
            temp = round(data['main']['temp'])
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            # Format kiểu quân sự, ngắn gọn
            return (f"🌡 Nhiệt độ: {temp}°C | ☁️ Tình trạng: {desc.capitalize()} | "
                    f"💧 Độ ẩm: {humidity}% | 💨 Gió: {wind_speed} m/s")
        else:
            logging.error(f"Weather API Error: {data}")
            return "Weather Data: Error fetching data."

    except Exception as e:
        logging.error(f"Weather Exception: {str(e)}")
        return "Weather Data: Connection failed."
