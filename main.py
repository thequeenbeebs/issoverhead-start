import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 37.168280  # Your latitude
MY_LONG = -113.681870  # Your longitude
EMAIL = "blairequeensmtp@yahoo.com"
PASSWORD = "eyckhyzvvmggmozc"

# Your position is within +5 or -5 degrees of the ISS position.


def iss_is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    lower_lat = MY_LAT - 5
    upper_lat = MY_LAT + 5
    lower_long = MY_LONG - 5
    upper_long = MY_LONG + 5
    close_latitude = lower_lat <= iss_latitude <= upper_lat
    close_longitude = lower_long <= iss_longitude <= upper_long
    return close_longitude and close_latitude


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    resp = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    resp.raise_for_status()
    data = resp.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    return time_now.hour >= sunset or time_now <= sunrise


while True:
    time.sleep(60)
    if iss_is_close() and is_night():
        with smtplib.SMTP('smtp.mail.yahoo.com') as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs='blairequeensmtp@gmail.com',
                msg="Subject: Look up!\n\nThe ISS is above you in the sky."
            )
# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

