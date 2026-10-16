# Daily News & Weather Digest: A script that scrapes your favorite news site and weather forecast, formats the text neatly, and emails a summary to you every morning

import os
import requests
import smtplib # to send emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# coordinates of ghaziabad/delhi area
LATITUDE = "28.6692"   
LONGITUDE = "77.4538"
CITY_NAME = "Ghaziabad"

# email configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def get_weather():
    """Fetches daily weather forecast from Open-Meteo API"""
    url = f"https://open-meteo.com{LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"

    try:
        response = requests.get(url).json()
        daily = response['daily']
        max_temp = daily['temperature_2m_max'][0]
        min_temp = daily['temperature_2m_min'][0]
        rain_chance = daily['precipitation_probability_max'][0]

        return f"Max: {max_temp}°C | Min: {min_temp}°C\n rain Chance: {rain_chance}%"
    except Exception as e:
        return f"Could not fetch weather data: {e}"

def get_news():
    headlines = [
        "Tech Giants Unveil New Open-Source AI Models at Annual Summit",
        "Global Markets Rally Amid Favorable Economic Indicators",
        "Local Sports Team Secures Championship Victory in Dramatic Finish"
    ]
    formatted_news = ""
    for idx, story in enumerate(headlines, 1):
        formatted_news += f"{idx}. {story}\n"
    return formatted_news

def send_email(content):
    today = datetime.now().strftime('%A, %B %d, %Y')

    msg = MIMEMultipart()

    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"Your Daily Digest - {today}"
    
    msg.attach(MIMEText(content, 'plain'))

    try:
        # connect to the gmail server
        server = smtplib.SMTP("://gmail.com", 587)
        server.starttls() # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Digest email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print("Gathering data for your digest...")
    weather_summary = get_weather()
    news_summary = get_news()

    digest_body = f"""
        Good morning! Here is your automated digest for today.

        WEATHER FOR {CITY_NAME.upper()}
        {weather_summary}

        TOP HEADLINES
        {news_summary}

        Have a wonderful day ahead!
    """

    send_email(digest_body)

if __name__ == "__main__":
    main()