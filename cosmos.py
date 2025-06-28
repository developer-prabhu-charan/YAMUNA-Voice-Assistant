import speech_recognition as sr
import pyttsx3
import subprocess
import time



listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

def talk(text):
    engine.say(text)
    engine.runAndWait()



listener.pause_threshold = 0.5
listener.energy_threshold = 700

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if command:
                command = command.lower()
    except Exception as e:
        print("In cosmos")
    if 'cosmos' in command:
        command = command.replace('cosmos', '').strip()
        if len(command)==0:
            talk("Yess sir..!")
        return command
    if 'yamuna' in command:
        subprocess.run(["python", "voice_Assist.py"])
        exit()

def execute_command(command):
    if 'artificial intelligence' in command:
        subprocess.Popen(["python", "automatedText.py"])
        time.sleep(2)
        talk("This is where, AI is going to go. So right now we are in the age of Generative AI. So generative AI is ChatGPT, Midjourney, you're generating music, art, text. We're coming to agentic AI. Agentic AI is AI that can actually think like an employee. It can solve complex problems without human intervention. So you can go to your Agentic AI and you will soon be able to say, listen, I run a real estate property company, I need a really interesting post to showcase my newest development. The AI will go analyze all the pictures in your Google Drive, pick the best pictures which are gonna create the best response, write a caption and come up with three different ideas, post three different ideas on TikTok, analyze, the data, generate the video, generate the voice, generate everything. And then see which one has the best response, and then turn that into a Facebook ad, put that ad on Facebook, tap into your credit card account, go and deploy money to Meta, to pay for the ad, analyze results of the ad, decide if it should kill it, expand it, tweak it, optimize it, then get back to you in 48 hours and say, here's my report. and it will do it better than any human employee, and it will do it, but may be 1 by 100 the cost. We are going in an age of instant results. you have heard of Software as a service, we are about to enter Results As A Service, RAAS. But that is just the beginning.")
    elif 'exit' in command:
        exit()




def run_cosmos():
    while True:
        command = take_command()
        if command:
            execute_command(command)

if __name__ == '__main__':
    print('This is Cosmos 1.0, I am ready to help you...!')
    talk('This is Cosmos 1 point O, I am ready to help you...!')
    run_cosmos()
