#############################################################
##  Wesley Vercoutere                                      ##
##  CVO Focus                                              ##
##  Deel 1: Basis programmeren in Python met RaspberryPi   ##
##  Les 7 - Oef 11                                         ##
#############################################################

'''
Oef 11 Gebruik je rotary encoder om een RGB waarde te genereren.
Draaien aan de rotary encoder verhoogt/verlaagt de waarde met +/- 5
Drukken op de rotary encoder verplaatst de keuze van R-G-B
Toon de waarde van RGB in 3 tekstvelden of labels in je GUI.
Toon het resultaat van de RGB selectie in je GUI door de kleur aan te passen en te tonen in een label.
'''
# https://python-reference.readthedocs.io/en/latest/docs/str/formatting.html

from tkinter import Tk, Label

try:
    import RPi.GPIO as GPIO
except:
    # from dummygpio.DummyGPIO import DummyGPIO
    # GPIO = DummyGPIO(True)
    print("No Raspberry Pi found")


root = Tk()
root.title('Les 7 - Oef 11')
root.geometry('800x400')

# GPIO general
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Inputs
pinPushBtn = 25
pinRotBtn = 13
pinRotA = 5
pinRotB = 6

inputs = [pinPushBtn, pinRotBtn, pinRotA, pinRotB]

GPIO.setup(inputs, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)




# Definitions
red = 0
green = 0
blue = 0
colors =[red, green, blue]
currentIndex = 0

MIN_NUMBER = 0
MAX_NUMBER = 255
STEP = 5


# Callbacks
def UpdateNumber(arg):
    global colors
    global currentIndex

    if arg:
        colors[currentIndex] += STEP
    else:
        colors[currentIndex] -= STEP

    if colors[currentIndex] > MAX_NUMBER:
        colors[currentIndex] = MIN_NUMBER
    
    if colors[currentIndex] < MIN_NUMBER:
        colors[currentIndex] = MAX_NUMBER


def TurnRotSensor(channel):
    statusRotB = GPIO.input(pinRotB)
    UpdateNumber(statusRotB)


def ChangeColor(channel):
    global currentIndex

    currentIndex += 1

    if currentIndex > 2:
        currentIndex = 0


GPIO.add_event_detect(pinRotA, GPIO.RISING, callback=TurnRotSensor, bouncetime=50)
GPIO.add_event_detect(pinRotBtn, GPIO.RISING, callback=ChangeColor, bouncetime=200)


# GUI
labelRedText = Label(root, text="Rood", padx=10, pady=10)
labelRedText.grid(row=0, column=0)
labelGreenText = Label(root, text="Groen", padx=10, pady=10)
labelGreenText.grid(row=0, column=1)
labelBlueText = Label(root, text="Blauw", padx=10, pady=10)
labelBlueText.grid(row=0, column=2)

labelsText = [labelRedText, labelGreenText, labelBlueText] 

labelRed = Label(root, text=red, padx=10, pady=10, fg="white")
labelRed.grid(row=1, column=0)
labelGreen = Label(root, text=green, padx=10, pady=10, fg="white")
labelGreen.grid(row=1, column=1)
labelBlue = Label(root, text=blue, padx=10, pady=10, fg="white")
labelBlue.grid(row=1, column=2)

labelsColor = [labelRed, labelGreen, labelBlue] 

labelColor = Label(root, text="color", padx=10, pady=10, fg="white")
labelColor.grid(row=2, column=1, padx=10, pady=10)


while True:
    root.update()

    for i in range(len(colors)):
        labelsText[i]['font'] = ('Helvetica', 18)
        
        if i == currentIndex:
            labelsText[i]['font'] = ('Helvetica', 18, 'bold')

    labelRed['bg'] = '#%02x%02x%02x' % (colors[0], 0, 0) 
    labelRed['text'] = str(colors[0])
    labelGreen['bg'] = '#%02x%02x%02x' % (0, colors[1], 0) 
    labelGreen['text'] = str(colors[1])
    labelBlue['bg'] = '#%02x%02x%02x' % (0, 0, colors[2]) 
    labelBlue['text'] = str(colors[2])
    labelColor['bg'] = '#%02x%02x%02x' % (colors[0], colors[1], colors[2]) 

