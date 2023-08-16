import tkinter as tk
import subprocess

def runESP32code():
    subprocess.run(["platformio", "run", "--target", "upload"])

def runPythonCode():
    subprocess.run(["python", r'C:\Users\dinos\Documents\PlatformIO\Projects\poskus\src\prepoznava.py'])

def runBoth():
    runESP32code()
    runPythonCode()

window = tk.Tk()

button = tk.Button(window, text="Run ESP32 and Python Code", command=runBoth)
button.pack()

window.mainloop()