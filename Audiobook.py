import pyttsx3
import keyboard
import PyPDF2
import threading
import os

pdf = None
stop_read = False
playback_thread = None

def play(pdfReader):
    global pdf
    global stop_read
    speaker = pyttsx3.init()
    for page in range(len(pdfReader.pages)):
        if stop_read == True:
            break
        txt = pdfReader.pages[page].extract_text()
        speaker.say(txt)
        speaker.runAndWait()
    speaker.stop()

def stop_playback():
    global stop_read
    global playback_thread
    input("Press Enter to stop playback")
    stop_read = True
    playback_thread.join()

def read_file():
    global pdf
    read_file_flag = 0
    while read_file_flag<3:
        file = input("Enter Filename: ")
        file = file + ".pdf"
        cwd = os.getcwd()
        if file in os.listdir(cwd):
            pdf = PyPDF2.PdfReader(file)
            return 1
        else:
            parent_directory = os.path.dirname(os.getcwd())
            if file in parent_directory:
                pdf = PyPDF2.PdfReader(file)
                return 1
            else:
                read_file_flag+=1
                print("No files Found")

def start_reading_thread():
    global playback_thread
    playback_thread = threading.Thread(target=play,args=(pdf,))
    playback_thread.start()

def stop_reading_thread():
    keyboard.add_hotkey("q", lambda: stop_playback())
    keyboard.wait()





if read_file():
    start_reading_thread()
    stop_reading_thread()

