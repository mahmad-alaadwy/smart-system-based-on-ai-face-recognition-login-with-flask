from flask import Flask,redirect,url_for,render_template,request
from tabnanny import check
import numpy as np
from sklearn import decomposition,datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle
import matplotlib.pyplot as plt
#save the file in pickle
import pickle
import collections
import face_recognition
import skimage.io
import cv2
import speech_recognition as sr
import pyttsx3
r=sr.Recognizer()


def speak():
    with sr.Microphone() as source2:
        r.adjust_for_ambient_noise(source2,duration=0.5)
        print("speak now")
        #isting to the user inputs
        audio=r.listen(source2)
        
        try:
            my_text=r.recognize_google(audio)
            my_text=my_text.lower()
            return my_text
                
        except:
            say_text("please say it again")
            speak()

        #using google to recognize the audio

def say_text(command,text=" "):
    engine=pyttsx3.init()
    engine.say(command)
    engine.say(text)
    engine.runAndWait()

def run_speach():    
    txt=speak()
    say_text("the system will search for",txt)
    print("you have said :",txt)
    return txt



def compare_unknoun_to_data_set(unknoun,data_set):
    results=[]
    for i in range(len(data_set)):
        res=face_recognition.compare_faces(data_set[i] ,unknoun)
        results.append(res)
    return results
def check_encodings(img):
    img=skimage.io.imread(img)
    unknown_encoding=[]
    unknown_encoding=face_recognition.face_encodings(img)[0]
    return unknown_encoding

def model(img):
    dataset=pickle.load(open('dataset','rb'))
    unknown_encoding=check_encodings(img)
    fet=dataset['faces_features']
    result=[]
    result=compare_unknoun_to_data_set(unknown_encoding,fet)
    count_esw=result[:548].count([True])
    count_ziad=result[584:].count([True])
    accuracy_of_being_eswy=count_esw/548
    accuracy_of_being_ziad=count_ziad/372
    if(accuracy_of_being_eswy>.88 or accuracy_of_being_ziad>.88):
        return True,(accuracy_of_being_eswy>accuracy_of_being_ziad)and'esawy' or 'ziad'
    else:
        return False,"is not a known"


def cuptuer():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("cupturing the image")
    img_counter = 0
    img_taked=True
    while img_taked:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("cupturing the image", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "checkimg.jpg"
            cv2.imwrite(img_name, frame)
            break

    cam.release()
    cv2.destroyAllWindows()
        

app = Flask(__name__)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        cuptuer()
        flag,user=model("checkimg.jpg")
        if(flag):
            return redirect(url_for("sys",useer=user))
        else:
            return redirect(url_for("unknown"))
    else:
        return render_template("index.html")


@app.route("/unknown")
def unknown():
    return f"<h1>{'un known user!'}</h1>"

@app.route("/<useer>",methods=['GET','POST'])
def sys(useer):
    return render_template("sys.html",user=useer)

@app.route("/system",methods=["POST"])
def system():
    return render_template("system.html")

@app.route("/systeem",methods=["POST"])
def speeek():
    say_text("welcome sir ask me any question and i will give you the answer")
    if request.method == "POST":
        txt=run_speach()
    txt_url="https://www.youtube.com/results?search_query="
    path=txt_url+txt
    print(path)
    return redirect(path)


if __name__=='__main__':
    app.run()

    