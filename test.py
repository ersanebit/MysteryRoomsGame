import tkinter as tk
import time

import winsound

def showImg():
    root = tk.Tk()
    image = tk.PhotoImage(file="key.png")
    label = tk.Label(image=image)
    label.pack()
    root.after(3000, lambda: root.destroy())
    root.mainloop()

def playSound():
    winsound.PlaySound('sound.mp3', winsound.SND_FILENAME)

playSound()
showImg()

# ring, earrings,