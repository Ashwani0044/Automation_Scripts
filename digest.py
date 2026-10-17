# Daily News & Weather Digest: A script that scrapes your favorite news site and weather forecast, formats the text neatly, and emails a summary to you every morning

import os
from datetime import datetime
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib # to send the email
import requests
from dotenv import load_dotenv
import feedparser 

load_dotenv()

# Coordinates for Ghaziabad
LATITUDE = "28.6692"   
LONGITUDE = "77.4538"
CITY_NAME = "Ghaziabad"

# Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def get_weather():
    """Fetches daily weather forecast from Open-Meteo API."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily = data['daily']
        max_temp = daily['temperature_2m_max'][0]
        min_temp = daily['temperature_2m_min'][0]
        rain_chance = daily['precipitation_probability_max'][0]

        return f"Max: {max_temp}°C | Min: {min_temp}°C | Rain Chance: {rain_chance}%"
    except Exception as e:
        return f"Could not fetch weather data: {e}"

def get_news():
    """Returns top headlines."""
    # headlines = [
    #     "Tech Giants Unveil New Open-Source AI Models at Annual Summit",
    #     "Global Markets Rally Amid Favorable Economic Indicators",
    #     "Local Sports Team Secures Championship Victory in Dramatic Finish"
    # ]
    # return "\n".join(f"{idx}. {story}" for idx, story in enumerate(headlines, 1))

    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"

    try:
        feed = feedparser.parse(rss_url)

        headlines = []
        for entry in feed.entries[:5]:
            headlines.append(entry.title)

        if not headlines:
            return "No news headlines found!"
        return "\n".join(f"{idx}. {story}" for idx, story in enumerate(headlines, 1))
    except Exception as e:
        return f"Could not fetch live news: {e}"


def send_email(content):
    """Sends the formatted digest email via SMTP."""
    today = datetime.now().strftime('%A, %B %d, %Y')

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"Your Daily Digest - {today}"
    
    msg.attach(MIMEText(content, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
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

    digest_body = dedent(f"""\
        Good morning! Here is your automated digest for today.

        WEATHER FOR {CITY_NAME.upper()}
        {weather_summary}

        TOP HEADLINES
        {news_summary}

        Have a wonderful day ahead!
    """)

    send_email(digest_body)

if __name__ == "__main__":
    main()


# using cronjob to automate the execution for 7 am daily
# 0 7 * * * /usr/bin/python3 /absolute/path/to/your/folder/digest.py >> /absolute/path/to/your/folder/digest.log 2>&1
# >> ... digest.log 2>&1: it appends any output errors or confirmation logs into a digest.log file so you can easily audit if it ran correctly while you were sleeping.