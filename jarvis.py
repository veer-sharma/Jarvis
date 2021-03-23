import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psutil
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import random
from requests import get
import pywhatkit as kit
import sys
import pyjokes
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import jarvisUi
from jarvisUi import Ui_MainWindow
import instaloader
from instaloader import instaloader

akashi_sentence = "Project(Akashi) by\n\nAbhishek C46\nSakshi\nAkanksha\nSonali"

#To wish
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning...")
    elif hour >= 0 and hour < 16:
        speak("Good Afternoon...")
    else:
        speak("Good Evening...")
    speak("I am Akashi. How may I help you?")

#News
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=2944b650ff6440019ddd085401c0789c'
    main_page = requests.get(main_url).json()
    #print(main_page)
    articles = main_page["articles"]
    #print(articles)
    head = []
    day = ["First", "Second", "Third", " Fourth", "Fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        #print(f"Today's {day[i]} news is:", head[i])
        speak(f"Today's {day[i]} news is {head[i]}")

# text to speech function
def speak(audio):
    # To convert text to speech
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 200)
    global akashi_sentence
    engine.say(audio)
    akashi_sentence = audio
    #print(audio)
    engine.runAndWait()  # without this command speech will not be audible to us

class MainThread(QThread):

    def run(self):
        self.TaskExecution()

    #to convert voice(microphone input) into text(string output)
    def takeCommand(self):
        #global sentence
        r = sr.Recognizer()
        with sr.Microphone() as source:
            global akashi_sentence
            akashi_sentence = "Listening..."
            print("listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            #audio = r.listen(source, timeout=4, phrase_time_limit=5)
        try:
            akashi_sentence = "Recognizing..."
            print("Recognizing...")
            self.query = r.recognize_google(audio, language='en-in') #using google for voice recognition
            #sentence = self.query
            print(f"user said: {self.query}\n")  # user query will be printed
            #speak(sentence)

        except Exception as e:
            #print(e)
            speak("Say that again please...")
            return "none"
        self.query = self.query.lower()
        return self.query

    def TaskExecution(self):
        time.sleep(2)
        wish()
        while True:
            self.query = self.takeCommand()
            # logic building for tasks
            if 'hello' in self.query or 'hi' in self.query:
                speak("Hello Sir, May I help you with something?")

            elif 'volume up' in self.query:
                pyautogui.press("volumeup")

            elif 'volume down' in self.query:
                pyautogui.press("volumedown")

            elif 'mute' in self.query:
                pyautogui.press("volumemute")

            elif 'battery' in self.query:
                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"The system has {percentage} percent battery")

            elif 'how are you' in self.query:
                speak("I am Fine. What about you?")

            elif 'thanks' in self.query or 'thank you' in self.query:
                speak("It\'s my pleasure")

            elif 'wikipedia' in self.query:
                speak("Searching Wikipedia...")
                self.query = self.query.replace("wikipedia ", "")
                results = wikipedia.summary(self.query, sentences=2)
                speak("According to wikipedia")
                #print(results)
                speak(results)

            elif 'open google' in self.query:
                speak("What should I search on google?")
                kit.search(self.takeCommand())

            elif 'play music' in self.query:
                music_dir = 'D:\\Music'
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                #print(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M")
                speak(f"the time is {strTime}")

            elif 'email' in self.query:
                speak("Ok, Whom should I send the email? Please enter his email id.")
                Main().showDialog()
                send_to_email = inpt
                #send_to_email = input('Enter the receiver\'s email id:')
                speak("what should I say?")
                self.query = self.takeCommand()
                if "send file" in self.query or "send attachment" in self.query:
                    email = 'sharma.rvasv.4@gmail.com'
                    password = '9920657433'
                    speak("okay,What is the subject for this email?")
                    self.query = self.takeCommand()
                    subject = self.query
                    speak("And sir, What is the message?")
                    self.query2 = self.takeCommand()
                    message = self.query2
                    speak("Please enter the correct path of file into the shell")
                    Main().showDialog()
                    file_location = inpt
                    #file_location = input("Please enter the path here")

                    speak("Please wait I am sending email now")

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    #setup the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment: filename= %s" % filename)

                    #Attach the attachment to MIMEMultipart object
                    msg.attach(part)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                    speak(f"Email has been sent to {send_to_email}")

                else:
                    email = 'sharma.rvasv.4@gmail.com'
                    password = '9920657433'
                    message = self.query
                    speak("okay,What is the subject for this email?")
                    self.query2 = self.takeCommand()
                    subject = self.query2

                    speak("Please wait I am sending email now")

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_email
                    msg['Subject'] = subject


                    msg.attach(MIMEText(message, 'plain'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                    speak(f"Email has been sent to {send_to_email}")

            elif 'open notepad' in self.query:
                npath = 'C:\Windows\system32\\notepad.exe'
                os.startfile(npath)

            elif 'close google' in self.query:
                speak("Closing Google...")
                os.system("taskkill /f /im iexplore.exe")

            elif 'close chrome' in self.query:
                speak("Closing Chrome...")
                os.system("taskkill /f /im chrome.exe")

            elif 'shutdown the system' in self.query:
                os.system("shutdown /s /t 5")

            elif 'restart the system' in self.query:
                os.system("shutdown /r /t 5")

            elif 'sleep the system' in self.query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif 'open command prompt' in self.query:
                os.system("start cmd")

            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    #k = self.takeCommand()
                    k = cv2.waitKey(50)
                    if k == 'close camera' or k == 27:
                        break;
                cap.release()
                cv2.destroyAllWindows()

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                print(ip)
                speak(f"your ip address is {ip}")

            elif 'send whatsapp' in self.query:
                speak("Please enter the number,whom you want to whatsapp")
                Main().showDialog()
                #phoneNum = inpt
                #print(phoneNum)
                speak("Ok, What should be the message?")
                whatMsg = self.takeCommand()
                whatHour = datetime.datetime.now().strftime("%H")
                whatMin = datetime.datetime.now().strftime("%M")
                kit.sendwhatmsg(f"+91{inpt}", whatMsg, int(whatHour), int(whatMin)+1)

            elif 'play song on youtube' in self.query:
                speak("Which song do u wanna play?")
                ys = self.takeCommand().lower()
                kit.playonyt(ys)

            elif 'close notepad' in self.query:
                speak("Closing Notepad")
                os.system("taskkill /f /im notepad.exe")

            elif 'close command prompt' in self.query:
                speak("Closing Command Prompt")
                os.system("taskkill /f /im cmd.exe")

            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif 'take ss' in self.query or 'take screenshot' in self.query:
                speak("what should be the name of this screenshot file?")
                name = self.takeCommand()
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("screenshot has been saved successfully. Now you may proceed with the next command.")

            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif 'close music' in self.query:
                speak("Closing Media player")
                os.system("taskkill /f /im wmplayer.exe")

            elif 'instagram profile' in self.query or 'profile on instagram' in self.query:
                speak("Please enter the username correctly")
                Main().showDialog()
                #name = inpt
                #name = input("Enter username here:")
                #url = f"https://www.instagram.com/{name}"
                gpath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                webbrowser.register('chrome',
                                    None,
                                    webbrowser.BackgroundBrowser(gpath))
                webbrowser.get('chrome').open(f"www.instagram.com/{inpt}")
                speak("Here is the profile you\'ve asked")
                time.sleep(5)
                speak("Do you want to download this profile picture?")
                condition = self.takeCommand()
                if "yes" in condition:
                    mod = instaloader.Instaloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("Profile picture is saved successfully. Now you may proceed with the next command")
                else:
                   pass

            elif 'tell me news' in self.query:
                speak("Please wait...\nfetching news...")
                news()

            elif 'quit' in self.query or 'exit' in self.query:
                speak("Thank you sir for using me.")
                exit()


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("../ironman.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("../T8bahf.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString('dd:MMM:yyyy')
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
        self.ui.textEdit.setText(akashi_sentence)

    def showDialog(self):
        global inpt, result
        inpt, result = QInputDialog.getText(self, 'Inputbox', 'Enter:')

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())