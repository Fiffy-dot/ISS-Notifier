import requests
from datetime import datetime
import time
import smtplib

MY_LAT = -1.970579
MY_LONG = -30.104429
my_email = "testfionamukuhi@gmail.com"
password = "TestCode24/7"


def close_to_ISS():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if -5 <= MY_LAT - iss_latitude <= 5 and -5 <= MY_LONG - iss_longitude <= 5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    hour_now = datetime.now().hour
    if hour_now >= sunset or hour_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_dark() and close_to_ISS():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email,password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
            )

