#!/usr/bin/env python3

"""
Creates a one-task timer. User can set time pause for work and for rest.
The timer will automatically loop through work time + rest time until the user
closes it.
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
from playsound import playsound
import os
import time

   
class Pomodoro(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.grid(row = 0, column = 0)

        self.continueFlag = True
        self.soundPath = os.path.join(os.path.dirname(__file__), \
                                      "multimedia/")
        self.soundPath = self.soundPath + "gong.mp3"
        
        self.workTime = tk.StringVar()
        self.workTime.set("25")  
        self.restTime = tk.StringVar()
        self.restTime.set("5")
        self.timerValue = tk.StringVar()

        self.setframe = ttk.Frame(self)
        self.timerframe = ttk.Frame(self)

        workLabel = ttk.Label(self.setframe, text = "Set work time, minutes")
        workLabel.grid(column = 0, row = 0, sticky =  tk.W)
        restLabel = ttk.Label(self.setframe, text = "Set rest time, minutes")
        workEntry = ttk.Entry(self.setframe, textvariable = self.workTime, \
                              width = 2)
        restEntry = ttk.Entry(self.setframe, textvariable = self.restTime, \
                              width = 2)
        runButton = ttk.Button(self.setframe, text = "Start", \
                               command = self.run_timer)
        self.timerLabel = ttk.Label(self.timerframe, \
                                    textvariable = self.timerValue)
        stopButton = ttk.Button(self.timerframe, text = "Stop", \
                                command = self.stop_timer)
        

        # grid for all elements
        for child in self.setframe.winfo_children():
            child.grid_configure(padx=10, pady=5)
        for child in self.timerframe.winfo_children():
            child.grid_configure(padx=10, pady=5)
        self.setframe.grid(column = 0, row = 0, sticky = tk.W + tk.E)
        self.timerframe.grid(column = 0, row = 1, sticky = tk.W + tk.E)
        restLabel.grid(column = 0, row = 1, sticky = tk.W)
        workEntry.grid(column = 1, row = 0, sticky = tk.W)
        restEntry.grid(column = 1, row = 1, sticky = tk.W)
        runButton.grid(columnspan = 2, row = 2)
        self.timerLabel.grid(row = 0, column = 0)
        stopButton.grid(column = 0, row = 1)
        self.timerframe.grid_forget()
        

    def check_data(self, *ignore):
        return self.workTime.get().isnumeric() and \
           self.restTime.get().isnumeric()

    def run_timer(self, *ignore):
        
        if not(self.check_data(self)):
            msg.showerror("Wrong time value", "Time should be given in minuts")
            return None
        self.continueFlag = True
        
        self.setframe.grid_forget()
        self.timerframe.grid()
        while self.continueFlag:
            wt = int(self.workTime.get()) * 60
            rt = int(self.restTime.get()) * 60
            while (wt > 0) and self.continueFlag:
                wt = wt - 1
                mins, secs = divmod(wt, 60)
                self.timerValue.set("Work lap: {:02d}:{:02d}".format(mins, secs))
                self.update()
                time.sleep(1)
            
            playsound(self.soundPath)
            while (rt > 0)  and self.continueFlag:
                rt = rt - 1
                mins, secs = divmod(rt, 60)
                self.timerValue.set("Rest lap: {:02d}:{:02d}".format(mins, secs))
                self.update()
                time.sleep(1)
           
        
    def stop_timer(self, *ignore):
        self.continueFlag = False
        self.setframe.grid()
        self.timerframe.grid_forget()


    def quit(self, event = None):
        self.continueFlag = True
        self.parent.destroy()

    
def main():
    main = tk.Tk()
    main.title("Pomodoro")
    mainframe = ttk.Frame(main).grid(column = 0, row = 0)
    window = Pomodoro(main)
    main.resizable(False, False)
    main.protocol("WM_DELETE_WINDOW", window.quit)
    main.mainloop()


if __name__ == "__main__":
    main()
