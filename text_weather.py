import schedule
import time
import requests
from twilio.rest import Client


# Getting data from Open-Meteo weather Api. Getting fields like temperature, apparent temperature, precipitation, chance of precipitation, and wind speed.
def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
    response = requests.get(url) # Get request
    data = response.json() # extracting JSON data from response
    return data 

def send_text(body):
    account_sid = ""   #Add you Twilio account information and the phone number you want to send the message to.
    auth_token = ""
    from_phone = ""
    to_phone = ""

    client = Client(account_sid, auth_token) # Creating Client object to interact with Twilio API


    message = client.messages.create( # sends the text message  
        body = body, # the body of the message
        from_= from_phone, # phone number that is sending the message(from Twilio)
        to= to_phone # phone number that is receiving the message
    )
    print("Text is sent!")

def send_weather():
    
    latitude = 44.986656  # longitude and lattitude for minneapolis, change it to your desired location
    longitude = -93.258133

    weather = get_weather(latitude, longitude) # Calling get_weather to get the weather data
    
    
    # Parsing through the JSON data to extract the desired values for each field. 
    # Ex of how it works, 'hourly' is a key in the 'weather' dictionary and 'temperature_2m' is a key within the 'hourly' dictionary.
    # It then retrieves the first element from that list, which is the temperature at the current hour.
    temp = weather["hourly"]["temperature_2m"][0]
    feels_like = weather["hourly"]["apparent_temperature"][0]
    precipitation_probability = weather["hourly"]["precipitation_probability"][0]
    precipitation = weather["hourly"]["precipitation"][0]
    wind_speed = weather["hourly"]["wind_speed_10m"][0]

    # Constructing the text message to be sent
    weather_message = (
        f"Current weather details in Minneapolis:\n"
        f"Temp: {temp:.2f}°F\n"
        f"Feels Like: {feels_like:.2f}°F\n"
        f"Chance of precipitation: {precipitation_probability:.2f}%\n"
        f"Amount of Precipitation: {precipitation:.2f} in\n"
        f"Wind Speed: {wind_speed} mph"
    )

    # Calling the send_text function to send the text
    send_text(weather_message)

# Scheduling the text to send at a certain time everyday
schedule.every().day.at("enter time in HH:MM format").do(send_weather)
while True: # Checking schdule and going to sleep for 5 seconds when running to reduce load on CPU.
    schedule.run_pending()
    time.sleep(5)

