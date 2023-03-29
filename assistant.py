import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import sys
from sys import platform
from twilio.rest import Client
from helpers import *
from system_operations import *
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

sys_ops = SystemTasks()
tab_ops = TabOpt()
win_ops = WindowOpt()

if __name__ == "__main__":
    # wishMe()
    # while True:
    if 1:
        # query = takeCommand().lower()
        # Logic for executing tasks based on query
        query='send message'
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                print("Your search name does not match any pages\n")

        elif 'terminate' in query:
            speak("goodbye! will meet you soon\n")
            print("goodbye! will meet you soon\n")
            exit()
        
        elif 'tweet' in query:
            speak("Please enter your Email ID")
            twitter()

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif 'search on youtube' in query:
            speak("What you want to search")
            content=takeCommand()
            youtube(content)

        elif 'location' in query:
            speak('What is the location?')
            location = takeCommand()
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.open(url)
            speak('Here is the location ' + location)

        elif 'news' in query:
            speak_news()

        elif "movies" in query:
            speak("Some of the latest popular movies are as follows :")
            get_popular_movies()
            
        elif "tv series" in query:
            speak("Some of the latest popular tv series are as follows :")
            get_popular_tvseries()
            
        elif 'tell me' in query:
            Query()

        elif 'show me an image' in query:
            speak("Tell me what image I will show you")
            text=takeCommand()
            generate_image(text)

        elif 'open google' in query:
            speak("opening google\n")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("opening stackoverflow\n")
            webbrowser.open("stackoverflow.com")   

        elif 'open twitter' in query:
            speak("opening twitter\n")
            webbrowser.open("twitter.com")

        elif 'open whatsapp' in query:
            speak("opening whatsapp\n")
            webbrowser.open("whatsapp.com")
        
        elif 'search' in query:
            speak('What do you want to search for?')
            search = takeCommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.open(url)
            speak('Here is What I found for' + search)
        
        elif 'screen context' in query:
            speak('Searching what is on your screen')
            print('Searching what is on your screen')
            screen_context()

        elif 'make a note' in query:
            speak("Tell me what to write")
            rememberMessage = takeCommand()
            if(rememberMessage!="None"):
                print("your notes\n"+rememberMessage)
                remember = open('data.txt', 'a')
                remember.write(rememberMessage)
                remember.close()
            else:
                print("You have not say anything\n")

        elif 'read my notes' in query:
            remember = open('data.txt', 'r')
            speak("reading notes" + remember.read())

        elif 'voice' in query:
            if 'female' in query:
                engine.setProperty('voice', voices[1].id)
            else:
                engine.setProperty('voice', voices[0].id)
            speak("Hello Sir, I have switched my voice.")
            print("Switching voice\n")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            print(f"Sir, the time is {strTime}")

        elif 'shutdown' in query:
            if platform == "win32":
                os.system('shutdown /p /f')
            elif platform == "linux" or platform == "linux2" or "darwin":
                os.system('poweroff')

        elif 'sleep' in query:
            sys.exit()

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'open paint' in query:                                                       
            os.system('mspaint')

        elif 'open notepad' in query:                                                         
            os.system('notepad')

        elif 'open explorer' in query:                                                        
            os.system('explorer')

        elif 'screenshot' in query:
            speak("taking screenshot")
            screenshot()

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = input("Enter Receiever Email ID\n")    
                sendEmail(to, content)
                speak("Email has been sent!")
                print("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry brother. I am not able to send this email")    

        elif "send message" in query:
                # You need to create an account on Twilio to use this service
                account_sid = 'AC9bc3340d93bb39eb2ddc3696f2af6b70'
                auth_token = 'fae7a9aa11d9d19c1bffc411d8e23e72'
                client = Client(account_sid, auth_token)
                Sender_No=input("Enter your number\n")
                Receiver_No=input("Enter your friend's number\n")
                try:
                    message = client.messages \
                                .create(
                                    body = "hello",
                                    from_=Sender_No,
                                    to =Receiver_No
                                )
                    print(message.sid)
                except:
                    print("Permission to send an SMS has not been enabled\n")

        elif "select" in query:
            time.sleep(1)
            sys_ops.select()
            
        elif "copy" in query:
            time.sleep(1)
            sys_ops.copy()
            
        elif "paste" in query:
            time.sleep(1)
            sys_ops.paste()
        
        elif "delete" in query:
            time.sleep(1)
            sys_ops.delete()
            
        elif "new file" in query:
            time.sleep(1)
            sys_ops.new_file()
        
        elif "save" in query:
            time.sleep(1)
            sys_ops.save()

        elif "switch tab" in query:
            tab_ops.switchTab()
    
        elif "close tab" in query:
            tab_ops.closeTab()

        elif "new tab" in query:
            tab_ops.newTab()
            
        elif "close window" in query:
            win_ops.closeWindow()
        
        elif "switch window" in query:
            win_ops.switchWindow()
            
        elif "minimize window"  in query:
            win_ops.minimizeWindow()
            
        elif "maximize window" in query:
            win_ops.maximizeWindow()
