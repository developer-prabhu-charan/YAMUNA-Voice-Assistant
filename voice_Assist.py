import datetime
import random
import speech_recognition as sr
import pyttsx3
import pywhatkit
import subprocess
import os
import time
import os
from google import genai
import shutil
import sys
import google.generativeai as genai
import os
import requests
import openai
from serpapi import GoogleSearch
import webbrowser
import cv2
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from dotenv import load_dotenv





load_dotenv()
api_key_Hidden = os.getenv("GEMINI_API_KEY")
if not api_key_Hidden:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")


genai.configure(api_key=api_key_Hidden)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 200,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)



tasks = []


synonyms1 = {
    'chrome': ['launch chrome', 'open google chrome', 'chrome'],
    'notepad': ['launch notepad', 'run notepad', 'notepad'],
    'calculator': ['launch calculator', 'run calculator', 'calculator', 'launch calc', 'run calc', 'calc'],
    'camera': ['launch camera', 'run camera', 'camera', 'launch cam', 'run cam', 'cam'],
    'file explorer': ['launch file explorer', 'run file explorer', 'file explorer', 'view files', 'file explorer', 'files', 'file manager'],
    'vlc': ['launch vlc', 'run vlc', 'chrome']
}

synonyms2 = {
    'hi': ['hello', 'hay', 'hey', 'hai', 'good morning', 'good afternoon', 'good evening'],
    'exit': ['bye', 'goodbye', 'stop', 'talk to you later', 'get you in a moment', 'good night']
}

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

def talk(text):
    engine.say(text)
    engine.runAndWait()



listener.pause_threshold = 0.9
listener.energy_threshold = 1000

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print("Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            if command:
                command = command.lower()
                if 'yamuna' in command:
                    subprocess.Popen(["python", "recog_anim.py"])
                    command = command.replace('yamuna', '').strip()
                    time.sleep(0.9)
                    if len(command)==0:
                        talk("Yess..!")
                    return command
                if 'cosmos' in command:
                    subprocess.run(["python", "cosmos.py",])
                    exit()
            else:
                pass
    except:
        pass
    

def set_volume(level = 10):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_volume = volume.GetMasterVolumeLevelScalar() * 100
        if (current_volume < level):
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            print(f"Volume increased to {level}%")
            talk(f"Volume increased to {level}%")
        else:
            volume.SetMasterVolumeLevelScalar(level / 100, None)
            print(f"Volume decreased to {level}%")
            talk(f"Volume decreased to {level}%")
    except Exception as e:
        print("Error setting volume")
        talk("No percentage mentioned to increase or decrease the volume")
        return

def set_brightness(level = 10):
    brightness = sbc.get_brightness(display=0)[0]
    try:
        if (brightness < level):
            sbc.set_brightness(level)
            print(f"Brightness increased to {level}%")
            talk(f"Brightness increased to {level}%")
        else:
            sbc.set_brightness(level)
            print(f"Brightness decreased to {level}%")
            talk(f"Brightness decreased to {level}%")
    except Exception as e:
        print("Error setting brightness")
        talk("No value mentioned to increase or decrease the brightness")
        return




def ask_chatgpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response['choices'][0]['message']['content']
        return answer.strip()
    except Exception as e:
        print("Error communicating with ChatGPT:", e)
        return "I'm sorry, I couldn't get a response from ChatGPT."

def ask_gemini(command):
    prompt = " ,Summarize the response, highlighting only the most important information.  Keep it concise and easy to understand in one paragraph."
    command = command + prompt
    print(command)
    try:
       response = chat_session.send_message(command)
       return response
    except Exception as e:
        print("Error generating text:", e)
        return "I'm sorry, I couldn't generate text based on your request."

def search_web(query):
    api_key = "7d9c8033b5b8af25b097bd8da772342d0d4b6915d5d8fbce91b28c1dbb2be0d2"
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": api_key
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        if "organic_results" in results:
            print(f"Search Results for '{query}':\n")
            for result in results["organic_results"][:3]:
                title = result.get("title", "No Title")
                detailed_snippet = result.get("detailed_snippet", "")
                snippet = result.get("snippet", "No Description Available")
                description = snippet or detailed_snippet or "No Description Available"
                link = result.get("link", "No Link")

                print(f"Title: {title}")
                print(f"Description: {description}")
                talk(title)
                talk(description)
                talk('This is the link')
                print(f"Link: {link}\n")
        else:
            print("No results found.")
    except Exception as e:
        print("Error:", e)


def greet_based_on_time1():
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good morning! How can I assist you today?")
    elif 12 <= hour < 18:
        talk("Good afternoon! How can I assist you today?")
    else:
        talk("Good evening! How can I assist you today?")

def greet_based_on_time2():
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good morning!. Nice to meet you!")
    elif 12 <= hour < 18:
        talk("Good afternoon!. Nice to meet you!")
    else:
        talk("Good evening!. Nice to meet you!")


def get_weather(city):
    api_key = 'e7bf2ee646917d4d75c4d7c3ef463f21'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response['cod'] == 200:
        weather = response['weather'][0]['description']
        temp = response['main']['temp']
        humidity = response ['main']['humidity']
        pressure = response['main']['pressure']
        print(f"The weather in {city} is currently {weather}, with a temperature of {temp:.2f}°C, a pressure of {pressure} hPa, and a humidity of {humidity}%.")
        talk(f"The weather in {city} is currently {weather}, with a temperature of {temp:.2f}°C, a pressure of {pressure} hPa, and a humidity of {humidity}%.")
    else:
        talk("Sorry, I couldn't retrieve the weather information.")

def tell_joke():
    joke = random.choice([
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ])
    talk(joke)

def add_task(task):
    tasks.append(task)
    talk(f"Task '{task}' added to your to-do list.")

def view_tasks():
    if tasks:
        talk("Your current tasks are: " + ', '.join(tasks))
    else:
        talk("Your to-do list is empty.")

def remove_task(task):
    if task in tasks:
        tasks.remove(task)
        talk(f"Task '{task}' removed from your to-do list.")
    else:
        talk(f"Task '{task}' not found.")


def get_news(location = 'india'):
    api_key = "0f53ca7b34c047e094fb14ea207e2f4b"
    url = "https://newsapi.org/v2/everything"
    print(location)
    if location.lower() == "telangana":
        params = {
            'q': 'Telangana',
            'apiKey': api_key,
            'sortBy': 'publishedAt',
            'language': 'en',
            
        }
        print(f"Top news for Telangana\n")
        talk("Top news for Telangana")
        
    elif location.lower() == "hyderabad":
        params = {
        'q': 'Hyderabad',
        'apiKey': api_key,
        'sortBy': 'publishedAt',
        'language': 'en',
        }
        print(f"Top news for Hyderabad\n")
        talk("Top news for hyderabad")
    else:
        params = {
            'country': 'in',
            'apiKey': api_key,
            'sortBy': 'publishedAt',
            'language': 'en',
        }
        print(f"Top news for Telangana, Hyderabad, and India:\n")
        talk("Top news for Telangana, Hyderabad, and India")
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data.get('articles', [])
        if articles:
            for index, article in enumerate(articles[:5]):
                print(f"{index + 1}. {article['title']}")
                talk(article['title'])
                print(f"   Source: {article['source']['name']}")
                talk(f"   Source: {article['source']['name']}")
                talk("published at ")
                print(f"   Published At: {article['publishedAt']}")
                talk("This is the link")
                print(f"   Link: {article['url']}\n")
        else:
            print("No news articles found for Telangana, Hyderabad, or India.")
            talk("No news articles found for Telangana, Hyderabad, or India.")
    else:
        print("Failed to fetch news:", response.status_code, response.text)
        talk("Failed to fetch news.")


def open(command):
    command = command.replace('open','').strip()
    try:
        if any(keyword in command for keyword in ['image', 'logo']):
            talk(f'opening {command}')
            webbrowser.open(f"https://www.google.com/search?hl=en&tbm=isch&q={command}")
        elif command:
            command_map = {
                'google': lambda query: webbrowser.open('https://www.google.com/search?q=' + query),
                'youtube': lambda query: webbrowser.open('https://www.youtube.com/results?search_query=' + query),
                'wikipedia': lambda query: webbrowser.open('https://en.wikipedia.org/wiki/' + query.strip()),
                'facebook': lambda query: webbrowser.open('https://www.facebook.com/' + query.strip()),
                'instagram': lambda query: webbrowser.open('https://www.instagram.com/' + query.strip()),
                'my channel': lambda query: webbrowser.open('youtube.com/@ppcprogrammerprabhucharan6691'),
                'chrome': lambda _: subprocess.Popen('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
                'notepad': lambda _: subprocess.Popen('notepad'),
                'camera': lambda _: os.system('start microsoft.windows.camera:'),
                'calculator': lambda _: subprocess.Popen('calc.exe'),
                'file explorer': lambda _: subprocess.Popen('explorer'),
                'vlc': lambda _: subprocess.Popen('C:\\Program Files\\VideoLAN\\VLC\\vlc.exe'),
            }
            for key in command_map:
                if key in command:
                    talk(f'Opening {command}')
                    query = command.replace(key, '').strip()
                    command_map[key](query)
                    return
        else:
            print("I'm sorry, I can't open that.")
            talk("I'm sorry, I can't open that.")
    except Exception as e:
        print(f"Error: {e}")

def execute_command(command):

    print(command)

    for action, aliases in synonyms1.items():
        if any(alias in command for alias in aliases):
            command = action
            open(command)
            command = ''
            break

    for action, aliases in synonyms2.items():
        if any(alias in command for alias in aliases):
            command = action
            break

    if any(keyword in command for keyword in ['play', 'youtube']):        
        print(command)
        command = command.replace('play', '').strip()
        print(command)
        talk(f'Playing {command}')
        pywhatkit.playonyt(command)

    elif 'take a photo' in command:
        talk(f'Opening camera and taking a photo in 5 seconds...')
        # Open the camera (0 = default camera)
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW for Windows to avoid MSMF issues

        if not camera.isOpened():
            print("Error: Could not access the camera.")
            talk('Error: Could not access the camera')
            return

        # Create a named window to display the feed
        cv2.namedWindow("Camera")
        
        # Frame counter to stop after capturing one photo
        frames_to_capture = 90  # Assuming 30 FPS, this will run for ~5 seconds
        frame_count = 0

        while frame_count < frames_to_capture:
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Display the live feed
            cv2.imshow("Camera", frame)

            # Increment frame count
            frame_count += 1

            # Wait for a short time (milliseconds) between frames
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break

        # Take the final photo
        ret, photo = camera.read()
        if ret:
            # Generate a unique filename using the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"photo_{timestamp}.jpg"
            cv2.imwrite(filename, photo)
            print(f"Photo saved as '{filename}'")
            talk('photo saved and closing camera')
        else:
            print("Error: Could not take a photo.")

        # Release the camera and close the window
        camera.release()
        cv2.destroyAllWindows()
    
    elif 'search' in command:
        prompt = command.replace('gemini', '').strip()
        if prompt:
            response = ask_gemini(prompt)
            cleaned_response = response.text.replace("*", "'").strip()
            print(cleaned_response)
            cleaned_response = response.text.replace("*", "").strip()
            talk(cleaned_response)
        else:
            pass


    elif 'open' in command:
        print("in open")
        open(command)

    elif "get" in command:
        query = command.replace("search", "").strip()
        talk(f"Searching for {query}")
        search_web(query)
    
    elif 'brightness' in command:
        if '%' in command:
            command = command.replace('%', '').strip()
        number = next((int(word) for word in command.split() if word.isdigit()), '')
        set_brightness(number)

    elif 'volume' in command:
        if '%' in command:
            command = command.replace('%', '').strip()
        number = next((int(word) for word in command.split() if word.isdigit()), '')
        set_volume(number)

    elif "news" in command:
        parts = command.split('in')
        if len(parts) > 1:
            city = parts[1].strip()
        else:
            city = 'hyderabad'
        talk(f"news in {city}")
        get_news(city)


    elif 'chart' in command:
                prompt = command.replace('chat', '').strip()
                if prompt:
                    response = ask_chatgpt(prompt)
                    print(response)
                    talk(response)
                else:
                    talk("Please provide a prompt for ChatGPT.")



    
    

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        talk(f'Current time is {current_time}')

    elif any(keyword in command for keyword in ['i love', 'love you']):
        talk('I love you three thousand times')

    elif 'exit' in command:
        print('Great time with you! Meet you again soon.')
        talk('Great time with you! Meet you again soon.')
        exit()

    elif 'hi' in command:
        greet_based_on_time1()

    elif 'shutdown' in command:
        talk('Confirm your password to shutdown')
        password = take_command()
        print(f'Password entered: {password}')
        if password == 'your password':
            talk('Shutting down your PC and closing all tasks.')
            os.system('shutdown /s /t 1')
            exit()
        else:
            talk('Access denied. Please try again.')

    elif any(keyword in command for keyword in ['he is', 'she is']):
        if 'she is' in command:
            command = command.replace('she is', '').strip()
            talk(f'Nice to meet you! {command}')
        else:
            command = command.replace('he is', '').strip()
            talk(f'Nice to meet you! {command}')

    elif 'tell me a joke' in command:
        tell_joke()

    elif 'weather' in command:
        parts = command.split('in')
        if len(parts) > 1:
            city = parts[1].strip()
        else: 
            city = 'hyderabad'
        get_weather(city)

    elif 'add task' in command:
        parts = command.split('task')
        if len(parts) > 1:
            task = parts[1].strip()
        print(task)
        add_task(task)

    elif any(keyword in command for keyword in ['view task', 'view tas']):
        print('in view tasks')
        view_tasks()

    elif 'remove task' in command:
        task = command.replace('remove task', '').strip()
        print('in remove tasks')
        remove_task(task)

    elif any(keyword in command for keyword in ['greet', 'wish']):
        greet_based_on_time2()
    
    elif len(command) == 0:
        pass

    else:
        print(f"{command} is not recognized as a valid command.")
        talk(f"{command}, is not a valid command.")

def run_yamuna():
    while True:
        command = take_command()
        if command:
            execute_command(command)

if __name__ == '__main__':
    subprocess.Popen(["python", "recog_anim.py"])
    print('This is Yamuna 3.O, I am ready to help you...!')
    talk('This is Yamna 3 point O, I am ready to help you...!')
    run_yamuna()