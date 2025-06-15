import os

import eel
import subprocess
from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():

    # This tells Eel where to look for the HTML/CSS/JS files (your UI is inside the www/ folder).
    eel.init("www")

#playing assistant sound
    playAssistantSound()
    @eel.expose
    def init():
        subprocess.call(r'device.bat') 
        eel.hideLoader()
        speak("ready for face authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face authentication successful")
            eel.hideFaceAuthSuccess()
            speak("Welcome , how may i help you")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face authentication fail")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)