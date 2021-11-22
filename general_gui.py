from tkinter import *

root = Tk()
root.title('Byzantine Generals Problem')
root.geometry("1280x720")


class GeneralGUI:
    def __init__(self, master):
        myFrame = Frame(master)
        myFrame.pack()

        self.myButton = Button(master, text="Click", command=self.clicker)
        self.myButton.pack(pady=20)

    def clicker(self):
        print("General")


e = GeneralGUI(root)
root.mainloop()
