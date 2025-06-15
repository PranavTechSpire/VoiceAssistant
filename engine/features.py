import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound 
import eel
import pvporcupine
import pyaudio
import pyautogui
import requests
from engine.command import speak
from engine.config import ASSISTANT_NAME
#Playing assistant sound function
import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat
@eel.expose  
#playing assistat start sound function
def playAssistantSound():
    music_dir = "www\\assets\\Audio\\start_sound.mp3"
    playsound(music_dir)
    
    
#opening various apps and web apps
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()
def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")
        

#playing something on youtube 
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on Youtube")
    kit.playonyt(search_term)


#Create function hotword in features file
    
import time  # Add this import
import struct
import pyaudio
import pvporcupine
import pyautogui

def hotword():
    try:
        # Initialize with proper key format
        porcupine = pvporcupine.create(
            keywords=["jarvis"],
            access_key='E10zwdJIQWMUmH1Cf8r8RSsVO1wSFZ0hnMqjXzWJC/NTP8D+RxIzpw==',  # Get from Picovoice Console
            sensitivities=[0.6]
        )
        
        paud = pyaudio.PyAudio()
        
        # Print available devices to verify
        print("Available audio devices:")
        for i in range(paud.get_device_count()):
            print(paud.get_device_info_by_index(i).get('name'))
            
        stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length,
            input_device_index=None  # Let PyAudio choose default
        )
        
        print(f"Listening for 'Jarvis' (Sample Rate: {porcupine.sample_rate})...")
        while True:
            try:
                pcm = stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h"*porcupine.frame_length, pcm)
                
                result = porcupine.process(pcm)
                if result >= 0:
                    print("Hotword detected!")
                    pyautogui.keyDown("win")
                    pyautogui.press("j")
                    time.sleep(2)
                    pyautogui.keyUp("win")
                    
            except IOError as e:
                print(f"Audio read error: {e}")
                # Reinitialize stream if needed
                stream.close()
                stream = paud.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length
                )
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        if 'stream' in locals(): 
            stream.close()
        if 'paud' in locals(): 
            paud.terminate()
        if 'porcupine' in locals(): 
            porcupine.delete()
# def hotword():
#     porcupine=None
#     paud=None
#     audio_stream=None
#     try:
       
#         # pre trained keywords    
#         porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
#         paud=pyaudio.PyAudio()
#         audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
#         # loop for streaming
#         while True:
#             keyword=audio_stream.read(porcupine.frame_length)
#             keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

#             # processing keyword comes from mic 
#             keyword_index=porcupine.process(keyword)

#             # checking first keyword detetcted for not
#             if keyword_index>=0:
#                 print("hotword detected")

#                 # pressing shorcut key win+j
#                 import pyautogui as autogui
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")          
#     except:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()


#### 8. Create find contacts number Function in features.py
# Whatsapp Message Sending
# def findContact(query):
 
#     words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
#     query = remove_words(query, words_to_remove)

#     try:
#         query = query.strip().lower()
#         cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#         results = cursor.fetchall()
#         print(results[0][0])
#         mobile_number_str = str(results[0][0])
#         if not mobile_number_str.startswith('+91'):
#             mobile_number_str = '+91' + mobile_number_str
#         return mobile_number_str, query
#     except:
#         speak('not exist in contacts')
#         return 0, 0

def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()
    
    try:
        cursor.execute("""
            SELECT name, mobile_no 
            FROM contacts 
            WHERE LOWER(name) LIKE ? OR mobile_no LIKE ?
            LIMIT 1
        """, (f'%{query}%', f'%{query}%'))
        
        result = cursor.fetchone()
        if result:
            name, mobile_no = result
            # Ensure proper international format
            if not mobile_no.startswith('+'):
                mobile_no = f'+91{mobile_no}'  # Default to India code
            return mobile_no, name
        return None, None
    except Exception as e:
        print(f"Contact search error: {e}")
        return None, None
    

#### 9. Create Whatsapp Function in features.py
def whatsApp(mobile_no, message, flag, name):
    """Improved WhatsApp automation function"""
    from urllib.parse import quote
    import subprocess
    import time
    import pyautogui
    import webbrowser
    
    try:
        # Validate mobile number format
        if not mobile_no.startswith('+'):
            mobile_no = f"+91{mobile_no}"  # Default to India code if no country code
        
        # Construct proper WhatsApp URL
        if flag == 'message':
            encoded_msg = quote(message)
            whatsapp_url = f"https://wa.me/{mobile_no}?text={encoded_msg}"
            jarvis_message = f"Message sent to {name}"
        elif flag == 'call':
            whatsapp_url = f"https://wa.me/{mobile_no}?voicecall=true" 
            jarvis_message = f"Calling {name}"
        else:  # video call
            whatsapp_url = f"https://wa.me/{mobile_no}?videocall=true"
            jarvis_message = f"Starting video call with {name}"

        # Open in default browser
        webbrowser.open(whatsapp_url)
        time.sleep(5)  # Wait for page to load

        # Perform action based on flag
        if flag == 'message':
            try:
                # Focus message box and send
                pyautogui.click(x=1000, y=1000)  # Adjust coordinates
                time.sleep(0.5)
                pyautogui.press('enter')  # Ensure focus
                time.sleep(0.5)
                pyautogui.press('enter')  # Send message
            except:
                speak("Message ready - please press enter to send")
        
        elif flag == 'call':
            try:
                pyautogui.click(x=1822, y=83)  # Call button
                time.sleep(1)
                pyautogui.click(x=900, y=400)   # Voice call
            except:
                speak(f"Please click call button to call {name}")
        
        elif flag == 'video':
            try:
                pyautogui.click(x=1764, y=92)  # Call button
                time.sleep(1)
                pyautogui.click(x=1100, y=400)  # Video call
            except:
                speak(f"Please click video button to call {name}")

        speak(jarvis_message)

    except Exception as e:
        print(f"WhatsApp error: {str(e)}")
        speak("Sorry, I couldn't complete the WhatsApp operation")
# def whatsApp(mobile_no, message, flag, name):

#     if flag == 'message':
#         target_tab = 8
#         jarvis_message = "message send successfully to "+name

#     elif flag == 'call':
#         target_tab = 7
#         message = ''
#         jarvis_message = "calling to "+name 

#     else:
#         target_tab = 6
#         message = ''
#         jarvis_message = "staring video call with "+name

#     # Encode the message for URL
#     encoded_message = quote(message)

#     # Construct the URL
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

#     # Construct the full command
#     full_command = f'start "" "{whatsapp_url}"'

#     # Open WhatsApp with the constructed URL using cmd.exe
#     subprocess.run(full_command, shell=True)
#     time.sleep(5)
#     subprocess.run(full_command, shell=True)
    
#     pyautogui.hotkey('ctrl', 'f')

#     for i in range(1, target_tab):
#         pyautogui.hotkey('tab')
#     pyautogui.hotkey('Enter')
#     speak(jarvis_message)


# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation
# def makeCall(name, mobileNo):
#     mobileNo =mobileNo.replace(" ", "")
#     speak("Calling "+name)
#     command = 'adb shell am start -a android.intent.action.CALL -d tel:+91'+mobileNo
#     os.system(command)
# def makeCall(name, mobileNo):
#     command = f'adb shell am start -a android.intent.action.CALL -d tel:{mobileNo}'
#     print("Executing:", command)  # Debugging
#     os.system(command)

# def adb_call(phone_number):
#     try:
#         # Remove spaces, hyphens just in case
#         phone_number = phone_number.replace(" ", "").replace("-", "")
#         print(f"Calling {phone_number} via ADB...")
#         os.system(f'adb shell am start -a android.intent.action.CALL -d tel:{phone_number}')
#     except Exception as e:
#         print("Failed to make call via ADB:", e)
#         speak("Call failed")


def make_adb_call(phone_number):
    """
    Make phone call via ADB
    Args:
        phone_number (str): Phone number in international format (e.g., +919876543210)
    """
    try:
        # Remove all non-digit characters except +
        cleaned_number = re.sub(r'[^\d+]', '', phone_number)
        
        # Validate phone number format
        if not re.match(r'^\+?[0-9]{10,15}$', cleaned_number):
            raise ValueError("Invalid phone number format")
            
        print(f"Attempting to call {cleaned_number} via ADB...")
        
        # ADB command to initiate call
        subprocess.run([
            'adb', 'shell', 
            'am', 'start', 
            '-a', 'android.intent.action.CALL', 
            '-d', f'tel:{cleaned_number}'
        ], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"ADB command failed: {e}")
        return False
    except Exception as e:
        print(f"Call failed: {e}")
        return False

    
def get_weather_forecast(day="today"):
    """Get weather forecast for specified day"""
    import requests
    import json
    from engine.config import WEATHER_API_KEY
    
    try:
        # Default city or implement location detection
        city = "Wagholi"
        
        # First get city coordinates
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"
        geo_response = requests.get(geo_url)
        geo_data = json.loads(geo_response.text)
        
        if not geo_data:
            return f"Could not find location data for {city}"
            
        lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
        
        # Get weather data - using current API endpoint
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(weather_url)
        data = json.loads(response.text)
        
        if day.lower() == "today":
            # Get first forecast (closest to current time)
            forecast = data['list'][0]
            day_str = "Today"
        elif day.lower() == "yesterday":
            return "Sorry, I can't provide yesterday's weather with the current API."
        elif day.lower() == "tomorrow":
            # Get forecast approximately 24 hours from now
            forecast = data['list'][8]  # 8*3h = 24h forecast
            day_str = "Tomorrow"
        else:
            return "Please specify 'today' or 'tomorrow'."
        
        # Parse weather data
        temp = forecast['main']['temp']
        weather_desc = forecast['weather'][0]['description']
        humidity = forecast['main']['humidity']
        
        return f"{day_str}'s weather in {city}: {weather_desc}, temperature {temp}°C, humidity {humidity}%"
        
    except Exception as e:
        print(f"Weather API error: {str(e)}")
        return "Sorry, I couldn't fetch the weather information."


import datetime
import threading
import time
from engine.command import speak
import eel
import re

def set_alarm(alarm_time_str):
    """
    Sets an alarm using a 12-hour format with AM/PM.
    Accepts flexible input like "7 am", "07:30 PM", "9:15pm", etc.
    """
    try:
        # Normalize input: remove extra spaces, add space before AM/PM if missing
        alarm_time_str = alarm_time_str.strip().upper()
        alarm_time_str = re.sub(r'(?<=[0-9])(?=AM|PM)', ' ', alarm_time_str)

        # Try to parse using datetime
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%I:%M %p") if ":" in alarm_time_str else datetime.datetime.strptime(alarm_time_str, "%I %p")

        now = datetime.datetime.now()
        alarm_datetime = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)

        if alarm_datetime <= now:
            alarm_datetime += datetime.timedelta(days=1)

        delay = (alarm_datetime - now).total_seconds()

        threading.Thread(target=alarm_thread, args=(delay, alarm_datetime.strftime("%I:%M %p"))).start()
        speak(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')}")

    except ValueError:
        speak("Please give the time in 12-hour format, like 7 AM or 10:30 PM.")

def alarm_thread(delay, time_str):
    time.sleep(delay)
    speak(f"⏰ Wake up! It's {time_str}")
    eel.DisplayMessage(f"⏰ Alarm: It's {time_str}")
