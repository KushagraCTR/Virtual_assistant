import speech_recognition as sr
import win32com.client
import datetime
import webbrowser
import random
import openai
from config import apikey
import os


chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr+=f"Kush: {query}\n Levi:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]



def ai(prompt):
    openai.api_key = apikey
    text= f"OpenAI response for Prompt:{prompt}\n***********************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text+= response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/prompt- {random.randint(1,23334567)}","w") as f:
        f.write(text)



def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")

    speaker.Speak(text)

def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio= r.listen(source)
        try:
            query= r.recognize_google(audio, language="en-in")
            print(f"User said:{query}")
        except Exception as e:
            return "Some Error Occurred. Sorry from Levi"
        return query

say("Hello I am Levi Ackerman...How can I help you master?")
while True:
    print("Listening")
    query= takeCommand()
    sites=[["youtube","https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google","https://www.google.com"]]
    for site in sites:
        if f"open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} Sir...")
            webbrowser.open(site[1])

    if "the time" in query:
        strfTime= datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir the time is {strfTime}")

    if "using Artificial intelligence".lower() in query.lower():
        ai(prompt=query)

    else:
        chat(query)

    #say(query)