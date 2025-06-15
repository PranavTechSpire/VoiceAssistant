
import pyautogui
import pyttsx3
import speech_recognition as sr
import eel


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 176)
    eel.DisplayMessage(text)
    # print(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        # print("listening...")
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1.5
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)

    try:
        # print('recognizing...')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en-in' )
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        speak(query)
        
    except Exception as e:
        return ""
    return query.lower()

# text = takecommand()

# speak(text)
@eel.expose
def allCommands(message=1):
    
    if message==1:
        query = takecommand()
        print(query) 
        eel.senderText(query)
    else:
        query = message 
        eel.senderText(query)
    
    try:
        # query = takecommand()
        # print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
#### 10. create whatsapp command in command.py
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            
            # Extract contact info with better error handling
            contact_no, name = findContact(query)
            
            if not contact_no or not name:
                speak("Contact not found")
                return

            # Determine action type
            if "send message" in query:
                action = 'message'
                speak("What message would you like to send?")
                message_content = takecommand()
                if not message_content or message_content.lower() == "none":
                    speak("Message cancelled")
                    return
            elif "phone call" in query:
                action = 'call'
                message_content = ""
            else:  # video call
                action = 'video'
                message_content = ""
            
            # Execute WhatsApp action
            whatsApp(contact_no, message_content, action, name)
                                
        elif "mobile call" in query:
            from engine.features import findContact, make_adb_call
            
            speak("Who would you like to call?")
            contact_query = takecommand()
            
            mobile_no, name = findContact(contact_query)
            if mobile_no:
                speak(f"Calling {name}")
                if make_adb_call(mobile_no):
                    speak(f"Connected to {name}")
                else:
                    speak("Failed to make the call")
            else:
                speak("Contact not found")
                
        elif "weather" in query or "forecast" in query:
            from engine.features import get_weather_forecast
            
            # Determine which day's weather is requested
            if "yesterday" in query:
                day = "yesterday"
            elif "tomorrow" in query:
                day = "tomorrow"
            else:
                day = "today"  # Default to today
            
            weather_report = get_weather_forecast(day)
            speak(weather_report)

        elif "set alarm" in query:
            from engine.features import set_alarm
            try:
                speak("At what time should I set the alarm?")
                alarm_input = takecommand()
                print("Alarm input:", alarm_input)
                set_alarm(alarm_input)
            except Exception as e:
                print("Alarm error:", e)
                speak("Sorry, I couldn't set the alarm.")

        else:
                # print("not run")
            from engine.features import chatBot
            chatBot(query)
    except:
        
        print("error...")

    eel.ShowHood()
    
