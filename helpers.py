import pyttsx3
import pyautogui
import psutil
import datetime
import pyjokes
import speech_recognition as sr
import requests
import geocoder
import smtplib
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import json
import wolframalpha
import time
import getpass
import os
import webbrowser
from urllib.request import urlopen
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from difflib import get_close_matches


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
g = geocoder.ip('me')
TMDB="your_api_key"
# data = json.load(open('data.json'))


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  
    weather()
    speak("I am Jarvis Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes microphone input from the user and returns string output
    time.sleep(3)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    youremail=input("Enter Your Email ID\n")
    password = getpass.getpass(prompt='Enter Your Gmail App Password\n')
    server.login(youremail,password)
    server.sendmail(youremail, to, content)
    server.close()

def speak_news():
    url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={your_api_key}'
    news = requests.get(url).text
    news_dict = json.loads(news)
    arts = news_dict['articles']
    speak('Source: The Times Of India')
    speak('Todays Headlines are..')
    k=0
    for index, articles in enumerate(arts):
        speak(articles['title'])
        if index == len(arts)-1 and k>3:
            break
        speak('Moving on the next news headline..')
        k+=1
    speak('These were the top headlines, Have a nice day Sir!!..')

def Query() -> None:
    client = wolframalpha.Client("your_api_key")
# ask the user for a query
    speak("What you want to know")
    ques = takeCommand()
    # ques="What is the value sin(90 degree)"
    res = client.query(ques)
# print the result
    for pod in res.pods:
        print(pod.title)
        for sub in pod.subpods:
            print(sub.plaintext)

def screen_context() ->None:
    filename=screenshot()
    url = 'https://api.ocr.space/parse/image'
    payload = {
        'apikey': 'your_api_key',
        'language': 'eng',
        'isOverlayRequired': False
    }
    with open(filename, 'rb') as image_file:
        r = requests.post(url, files={'image': image_file}, data=payload)

    text = r.json()['ParsedResults'][0]['ParsedText']
    speak(text)
    print(text)

def generate_image(text):
    stability_api = client.StabilityInference(
        key="your_api_key",
        verbose=True,
    )
    # the object returned is a python generator
    answers = stability_api.generate(
        prompt=text,
        seed=95456,
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("WARNING: Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
                return
            elif artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.show()

def screenshot() -> str:
    img = pyautogui.screenshot()
    path = "C:/ScreenShots"
    os.mkdir(path)
    file=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename=path + '\\'+ file + '.png'
    img.save(filename)
    return filename


def cpu() -> None:
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)
    print("CPU is at"+usage)
    
    battery = psutil.sensors_battery()
    speak("battery is at")
    print("battery is at")
    speak(battery.percent)
    print(battery.percent)

def joke() -> None:
    for i in range(1):
        speak(pyjokes.get_jokes()[i])
        print(pyjokes.get_jokes()[i])

def twitter() -> None:
    email = input("Enter Email ID\n")
    driver = webdriver.Chrome()
    driver.get("https://twitter.com/i/flow/login")
    wait = WebDriverWait(driver, 20)
    emailn = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    emailn.send_keys(email)

    input("Press enter to close the browser")
    driver.quit()
    speak("Your tweet has been sent")

def youtube(textToSearch):
    if(textToSearch=="None"):
        speak("You have not say anything")
    else:
        query = urllib.parse.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(url)

def weather():
    api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
        str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

    data = requests.get(api_url)
    data_json = data.json()
    if data_json['cod'] == 200:
        main = data_json['main']
        wind = data_json['wind']
        weather_desc = data_json['weather'][0]
        speak(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
        speak('Current location is ' + data_json['name'] + data_json['sys']['country'])
        print('Current location is ' + data_json['name'] + data_json['sys']['country'])
        speak('weather type ' + weather_desc['main'])
        speak('Wind speed is ' + str(wind['speed']) + ' metre per second')
        speak('Temperature: ' + str(main['temp']) + 'degree celcius')
        speak('Humidity is ' + str(main['humidity']))

def get_popular_movies():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for movie in response["results"]:
            title = movie['title']
            print(title)
    except KeyError:
        return None

def get_popular_tvseries():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for show in response["results"]:
            title = show['name']
            print(title)
    except KeyError:
        return None