import urllib.request
import os

from tkinter import *
from customtkinter import *

from PIL import Image, ImageTk
from pathlib import Path

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


def get_friends():
    driver = automation.ava_brauser()
    automation.logi_sisse(driver)
    return automation.sõbrad(driver)


images = list()


def load_friends():
    images.clear()
    home = Path.home()
    path = home.joinpath("facebookBirthdayWisher", "pictures")
    path.mkdir(parents=True, exist_ok=True)  # if folder doesn't exist create it

    image_files = Path(path).glob("*")

    for file in image_files:
        img = Image.open(file)
        img.resize((50, 50))
        photo_image = ImageTk.PhotoImage(img)
        images.append(photo_image)

        image_label = Label(objFrame, image=photo_image)
        image_label.grid(row=int(file.name[3:-4]), column=0, pady=10, padx=10)

    name_list = []
    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip():
                name_list.append((line_as_list[0], line_as_list[1], line_as_list[2] == "True"))

    for i in range(len(name_list)):
        name_label = Label(objFrame, text=name_list[i][0])
        name_label.grid(row=i, column=1, pady=10)

        checkbox = CTkCheckBox(objFrame, text="")
        checkbox.grid(row=i, column=2, pady=10)

    return name_list


def update_friends(friend_list):
    images.clear()
    home = Path.home()
    home.joinpath("facebookBirthdayWisher", "pictures").mkdir(parents=True,
                                                              exist_ok=True)  # create folder to store images

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        old_list = []

        # create list of tuples with the following format: (name, custom birthday wish, True/False - is automatic birthday wishing turned on for this person)
        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip():
                old_list.append((line_as_list[0], line_as_list[1], line_as_list[2] == "True"))

    new_list = []

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "w", encoding="UTF-8") as f:
        for i in range(len(friend_list)):
            custom_wish = ""
            active = "False"
            for item in old_list:
                if friend_list[i].get("nimi") == item[0]:
                    # copy over active status and custom wish from old friend list
                    custom_wish = item[1]
                    if item[2]:
                        active = "True"

            f.write(friend_list[i].get("nimi") + ";" + custom_wish + ";" + active + os.linesep)
            new_list.append((friend_list[i].get("nimi"), custom_wish, active == "True"))

    for i in range(len(friend_list)):
        path = str(home.joinpath("facebookBirthdayWisher", "pictures")) + os.sep + "pic" + str(i) + ".jpg"
        urllib.request.urlretrieve(friend_list[i].get("pilt"), path)
        img = Image.open(path)
        img.resize((50, 50))
        photo_image = ImageTk.PhotoImage(img)
        images.append(photo_image)

        image_label = Label(objFrame, image=photo_image)
        image_label.grid(row=i, column=0, pady=10, padx=10)

        name_label = Label(objFrame, text=friend_list[i].get("nimi"))
        name_label.grid(row=i, column=1, pady=10)

        checkbox = CTkCheckBox(objFrame)
        checkbox.grid(row=i, column=2, pady=10)

    root.update()
    return new_list


#  update frame layout after loading friends
root.update()
load_friends()

root.mainloop()
