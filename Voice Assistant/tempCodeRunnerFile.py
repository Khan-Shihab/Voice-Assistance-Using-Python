import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
import datetime
from googletrans import Translator
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()

API_KEY = "4d7f3555382e0b13a86f6a2ea29d1271"
openai.api_key = "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"
news_api = "7580ad7563e04f4b85426cb97dca9910"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def check_weather_alert(city):
    weather_info = get_weather(city)
    if "rain" in weather_info:
        speak("Rain is expected, take an umbrella!")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "ok":
        articles = data['articles']
        for article in articles[:1]:  # Display top 5 articles
            title = article['title']
            description = article['description']
            url = article['url']
            print(f"Title: {title}")
            print(f"Description: {description}")
            print(f"URL: {url}\n")
            speak(f"Title: {title}. Description: {description}")
    else:
        speak("Sorry, I couldn't fetch the news.")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # Make the GET request to the OpenWeatherMap API
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Check if the API call was successful (status code 200)
    if data["cod"] == 200:
        temp = data["main"]["temp"]  # Temperature
        description = data["weather"][0]["description"]  # Weather condition
        return f"The current temperature in {city} is {temp}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather details."

def get_gpt_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": prompt}],  
        max_tokens=100
    )  
    return response.choices[0].text.strip()


def tell_time():
    current_time = datetime.datetime.now().strftime("%H:%M")
    speak(f"The time is {current_time}")

def tell_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {current_date}")

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    speak(f"The translation is {translation.text}")

def open_application(app_name):
    if app_name.lower() == "chrome":
        os.system("start chrome")
    elif app_name.lower() == "vs code":
        os.system("start code")
        
def processCommand(c):
    print(c)                
    if c.lower() == "open google":
        webbrowser.open("https://www.google.com/") 
    elif c.lower() == "open youtube":
        webbrowser.open("https://www.youtube.com/") 
    elif c.lower() == "open codeforce":
        webbrowser.open("https://codeforces.com/") 
    elif c.lower() == "open facebook":
        webbrowser.open("https://facebook.com/") 
    elif c.lower() == "news":
        get_news()
    elif c.lower() == "weather":
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source: 
                speak("Which place?")
                print("Listening...") 
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print(word)
            weather_info = get_weather(word)  
            print(weather_info)
            speak(weather_info)  
            check_weather_alert(word)
        except Exception as e:
            print(f"Error: {e}")

    elif c.lower() == "time":
        tell_time()

    elif c.lower() == "date":
        tell_date()
    else:
        output = get_gpt_response(c)
        speak(output) 

        
if __name__ == "__main__":

    while True:
        r = sr.Recognizer()
        
        # Recognizing speech 
        try:
            with sr.Microphone() as source:  # speech recognizer
                speak("Call name")
                print("Listening...") 
                audio = r.listen(source)
            word = r.recognize_google(audio)
            print(word)
            if word.lower() == "rabia" or word.lower() == "rabiya":
                with sr.Microphone() as source:  # listen for command
                    print("rabia active") 
                    speak("Yes sir, how can I help you?")
                    audio = r.listen(source)        
                    command = r.recognize_google(audio)  
                    processCommand(command)    
            elif word.lower() == "exit":
                break
        except Exception as e:
            print(f"error; {e}")
