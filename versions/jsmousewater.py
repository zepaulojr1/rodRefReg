#____________REQUIRED_PACKAGES________________________________________________________________________________________________________>
import RPi.GPIO as GPIO # Allows for control over the RP's GPIO pins
import time # Importing system time etc.
import tkinter as tk # UI
import PIL
from PIL import Image, ImageTk
import threading # Using threading to prevent the run program loop from preventing the main event loop from executing
import datetime #for adding timecodes to print statements

import sm_16relind
rel = sm_16relind.SM16relind(0)
rel.set_all(15)


#____________DEFINING_KEY_VARIABLES___________________________________________________________________________________________________>
selected_pins = []  # List to store selected relay pins
INTERVAL = 3600  # Default interval: 1 hour
STAGGER = 1  # Default stagger: 1 second (between pump signals
WINDOW_START = 8  # Default window start time: 8 AM
WINDOW_END = 20  # Default window end time: 8 PM
running = False


#____________GPIO_NUMBERING_SYSTEM_SETUP______________________________________________________________________________________________>
# Setting up the GPIO numbering mode to use the RP's native BCM numbering system for the GPIO pins.
# This is needed because the GPIO pins on the RP are not numbered sequentially. In addition, only 26 of the 40 are actually usable for>
## The 14 others include the 5V, 3V inputs, and several grounds.
## 3 more pins (of the 26 remaining) are also taken up by the 16-relays hat (see below for details)

GPIO.setmode(GPIO.BOARD)


#____________DEFINING_PINS_AVAILABLE_FOR_CONNECTION_TO_RELAYS_________________________________________________________________________>
# From SequentMicrosystems: 16-relays hat takes up 3 GPIO pins (2,3 as the 12C port pins, and 26 for the pushbutton).
## As such, I need to arbitrarily choose 16 of the remaining free pins to connect to each of the hat's 16 relays.
### I also needed to skip over pins that aren't set up for GPIO, since I'm using GPIO.BOARD NOW (see written doc I made)

###UPDATE: I have learned that the GPIO pins must be connected to the COM terminals of each relay in order to trigger them. 
##Since each COM terminal is responsible for two relays, the relays must be triggered in pairs. 
# As such, I only need 8 free GPIO PINS!!

RELAY_PINS = [8, 10, 12, 16, 18, 22, 24, 32]

# The first GPIO pin listed will correspond to Relay 1 and so forth. I have created a legend listed below:
# PIN 8 -- Relay 1
# PIN 10 -- Relay 2
# PIN 12 -- Relay 3
# PIN 16 -- Relay 4
# PIN 18 -- Relay 5
# PIN 22 -- Relay 6
# PIN 24 -- Relay 7
# PIN 32 -- Relay 8

#___________RELAY_NAME_DICTIONARY_____________________________________________________________________________________________________>
# This will make things simpler in the UI by changing the relay names to the relay number instead if the GPIO Pin number connected to >
RELAY_NAMES = {
        8: "Relays 1 & 2 (P8)",
        10: "Relays 3 & 4 (P10)",
        12: "Relays 5 & 6 (P12)",
        16: "Relays 7 & 8 (P16)",
        18: "Relays 9 & 10 (P18)",
        22: "Relays 11 & 12 (P22)",
        24: "Relays 13 & 14 (P24)",
        32: "Relays 15 & 16 (P32)",
}

#_____________WATERPUMP_CLASS_________________________________________________________________________________________________________>
# Below I am creating the waterpump class to control the logic for each pump (i.e., for each GPIO PIN connected to a relay on the hat)
# "__init__" is called to initialize each water pump object with their respective GPIO pin ("pump_pin"). This will declare the pins as>
# The "trigger" method activates each pump by setting their corresponding GPIO pin to high.
## GPIO.HIGH allows current to flow through the pin, while GPIO.LOW does not.

class WaterPump:
        def __init__(self, relay_pin):
                self.relay_pin = relay_pin
                GPIO.setup(self.relay_pin, GPIO.OUT)
                GPIO.output(self.relay_pin, GPIO.LOW)  # This makes sure the relay is initially off

        def trigger(self):
                relay_name = RELAY_NAMES.get(self.relay_pin, f"Relay (Pin {self.relay_pin})")
                GPIO.output(self.relay_pin, GPIO.HIGH)  # Activate the relay to turn on the pump
                print (f"{datetime.datetime.now()} - Pumps connected to {relay_name} triggered")
                time.sleep(1)  # Arbitrary Time Delay, may need to adjust later as needed.
                GPIO.output(self.relay_pin, GPIO.LOW)  # Turns off the relay

# This makes different instances of WaterPump for each relay pin using the free GPIO pins I defined above
pumps = [WaterPump(pin) for pin in RELAY_PINS]


#___________VARIABLES_THAT_THE_USER_CAN_ALTER_________________________________________________________________________________________>

def toggle_pin(pin):
    relay_number = RELAY_NAMES.get(pin, f"{datetime.datetime.now()} - Relay connected to PIN {pin}")  # Gets the relay number from the>
    if pin in selected_pins:
        selected_pins.remove(pin)
        print(f"{datetime.datetime.now()} - {relay_number} turned off")
    else:
        selected_pins.append(pin)
        print(f"{datetime.datetime.now()} - {relay_number} turned on")

def update_interval():
        global INTERVAL
        try:
                INTERVAL = int(interval_entry.get())
                print (f"{datetime.datetime.now()} - Interval Updated")
        except ValueError:
                messagebox.showerror("Error", "Please enter a valid interval value (integer)")

def update_stagger():
        global STAGGER
        try:
                STAGGER = int(stagger_entry.get())
                print (f"{datetime.datetime.now()} - Stagger Time Updated")
        except ValueError:
                messagebox.showerror("Error", "Please enter a valid stagger value (integer)")

def update_window():
        global WINDOW_START, WINDOW_END
        WINDOW_START = int(window_start_entry.get())
        WINDOW_END = int(window_end_entry.get())
        print (f"{datetime.datetime.now()} - Watering Window Updated")

def run_program():
        global running
        running = True
        threading.Thread(target=program_loop).start() # To not mess with other aspects of the main loop
        print (f"{datetime.datetime.now()} - Program Started")

def stop_program():
        global running
        running = False
        rel.set_all(0)
        root.destroy()
        print (f"{datetime.datetime.now()} - Program Stopped")

#____________MEAT_AND_POTATOES________________________________________________________________________________________________________>
# Below is the main loop that runs indefinitely until the program is terminated using "KeyboardInterrupt" or by usingthe exit program >
# In the loop, the current system time is checked, and the pumps are triggered if the current time matches the specified time interval>
## This is done by taking the modulus of "current_time" and "interval".

# The loop repeats every second to see if its time to trigger the pumps again.

# JJC Note: don't have to check 1000 a second your checking on the clock of the raspberry Pi

def program_loop():
        global running
        try:
                GPIO.setmode(GPIO.BOARD)
                while running:
                        current_hour = time.localtime().tm_hour # This is to retrieve the current hour
                        if WINDOW_START <= current_hour < WINDOW_END: # To ensure water is only provided during set hours (mices' nigh>
                                current_time = time.time()
                        if current_time % INTERVAL < 1: # Determining whether it's time to trigger the pumps
#JJC Note what about <= 1, is this a datetime object? cast to float? Indent to be inside the previous If stat>
                                                for pump in pumps:
                                                    if pump.relay_pin in selected_pins:
                                                        pump.trigger()
                                                        time.sleep(STAGGER) # Staggers the pump triggers with user-decided value
                                                time.sleep(1) # Checks again every sec
        except KeyboardInterrupt: # This command defaults to CTRL+C, if the Exit Program button stops working
                print (f"{datetime.datetime.now()} - Exiting Program")
        finally:
                GPIO.cleanup() # Avoids a runtime error (see more details below)



# ______________USER__INTERFACE__STUFF________________________________________________________________________________________________>

# Generating the GUI
root = tk.Tk()
root.title("Rodent Refreshment Regulator")

# For Toggling relay pins on/off in the UI, and making sure the *actual relay number is displayed (not the stupid pre-loaded numbering>
toggle_frame = tk.Frame(root)
toggle_frame.pack()
# This makes it so the first 8 checkboxes (for each relay) appear on top of the other 8. This will keep the UI window from being ridic>
for i in range(8):
    pin = RELAY_PINS[i]
    name = RELAY_NAMES.get(pin, f"PIN no.{pin}") # This gets the dictionary name from above or defaults the name to "Pin no.X"
    tk.Checkbutton(toggle_frame, text=name, command=lambda p=pin: toggle_pin(p)).grid(row=0, column=i)
for i in range(8, len(RELAY_PINS)):
    pin = RELAY_PINS[i]
    name = RELAY_NAMES.get(pin, f"PIN no.{pin}") # see above
    tk.Checkbutton(toggle_frame, text=name, command=lambda p=pin: toggle_pin(p)).grid(row=1, column=i-8)

# UI for specifying the interval
interval_frame = tk.Frame(root)
interval_frame.pack()
tk.Label(interval_frame, text="Interval (seconds):").grid(row=0, column=0)
interval_entry = tk.Entry(interval_frame)
interval_entry.insert(0, INTERVAL)
interval_entry.grid(row=0, column=1)
tk.Button(interval_frame, text="Apply", command=update_interval).grid(row=0, column=2)

# Stagger UI
stagger_frame = tk.Frame(root)
stagger_frame.pack()
tk.Label(stagger_frame, text="Stagger (seconds):").grid(row=0, column=0)
stagger_entry = tk.Entry(stagger_frame)
stagger_entry.insert(0, STAGGER)
stagger_entry.grid(row=0, column=1)
tk.Button(stagger_frame, text="Apply", command=update_stagger).grid(row=0, column=2)

# Window entry UI
window_frame = tk.Frame(root)
window_frame.pack()
tk.Label(window_frame, text="Water Window Start (24-hour format):").grid(row=0, column=0)
window_start_entry = tk.Entry(window_frame)
window_start_entry.insert(0, WINDOW_START)
window_start_entry.grid(row=0, column=1)
tk.Label(window_frame, text="Water Window End (24-hour format):").grid(row=1, column=0)
window_end_entry = tk.Entry(window_frame)
window_end_entry.insert(0, WINDOW_END)
window_end_entry.grid(row=1, column=1)
tk.Button(window_frame, text="Apply", command=update_window).grid(row=1, column=2)

# Warning label for closing the program
warning_message = "*Only close the program via the 'Stop Program' Button. Closing the window via the top right will cause errors. CTRL+C closes everything if needed"
warning_label = tk.Label(root, text=warning_message, fg="red")
warning_label.pack()

# Run button
run_button = tk.Button(root, text="Run Program", command=run_program)
run_button.pack()

# Stop button
stop_button = tk.Button(root, text="Stop Program", command=stop_program)
stop_button.pack()

# Defining the image paths
image1 = Image.open("/home/conelab/lablogo.jpg")
image2 = Image.open("/home/conelab/rockmouse.jpg")

# Resizing the beautiful rock image
image2 = image2.resize((200,200), Image.LANCZOS)

# Converting the pictures to be compatible with tkinter
tk_image1 = ImageTk.PhotoImage(image1)
tk_image2 = ImageTk.PhotoImage(image2)

# Defining the labels needed to display the images
left_image_label = tk.Label(root, image=tk_image1)
left_image_label.pack(side=tk.LEFT)

right_image_label = tk.Label(root, image=tk_image2)
right_image_label.pack(side=tk.RIGHT)

#Placing the two pictures side by side underneath the stop button  (so that they don't appear off screen like before)
left_image_label.pack(side=tk.TOP)
right_image_label.pack(side=tk.BOTTOM)


#__________GPIO_CLEANUP_IF_PROGRAM_IS_CLOSED_INCORRECTLY______________________________________________________________________________>

try:
        root.mainloop()
finally:
        GPIO.cleanup() # once the root destroy command has been executed via clicking the stop program button, this clears the GPIO pins


### TO DO
# PUSHBUTTON INCORPORATION TO PREVENT SD CARD FAILURE (PLUS A UI ELEMENT INDICATING HOW THE USER NEEDS TO DO THIS
# EMAIL AUTOMATION FOR IF THE PROGRAM SUDDENLY STOPS
# LEARN HOW TO STACK THE CARDS IF NEEDED (FOR THE PAPER)
# FIX UI WINDOW SIZE AND SCROLLING ETC.
# GO THROUGH AND INCORPORATE ALL REMAINING JJC EDITS


# UPDATE FEB 29:
# Relays turn on/off the voltage you provide, they do not amplify. as such, I can go back to a version of the program that just triggers the GPIO pins. No need for relays pairs etc.
