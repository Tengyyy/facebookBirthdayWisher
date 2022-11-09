from tkinter import *
from customtkinter import *

import automation
from ScrollableFrame import ScrollableFrame

set_appearance_mode("Dark")
set_default_color_theme("blue")

root = CTk()
root.geometry("400x580")
root.title("Facebooki automaatne õnnesoovija")
root.iconbitmap("Resources/icon.ico")

obj = ScrollableFrame(root, mousescroll=10)

objFrame = obj.frame


def saa_sobrad():
    driver = automation.ava_brauser()
    automation.logi_sisse(driver)
    return automation.sõbrad(driver)


root.update()

friends = saa_sobrad()
for i in range(len(friends)):
    label = Label(objFrame, text=friends[i].get("nimi"))
    label.grid(row=i, column=0, pady=10, padx=10)

#  update frame layout after loading friends

root.update()

root.mainloop()
