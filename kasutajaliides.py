import urllib.request

from tkinter import *
from customtkinter import *

from PIL import Image, ImageTk
from pathlib import Path

import automation
from ScrollableFrame import ScrollableFrame

import os
import shutil


def search():
    searchword = search_box.get()

    for i in range(len(objFrame.winfo_children())):
        if i >= 1:
            objFrame.winfo_children()[1].destroy()

    counter = 1
    for friend in all_friends:

        if searchword in friend.get("name").lower():
            image_label = Label(objFrame, image=friend.get("image"), background="#1E1E1E")
            image_label.grid(row=counter, column=0, pady=10, padx=10)

            name_label = Label(objFrame, text=friend.get("name"), background="#1E1E1E", foreground="white")
            name_label.grid(row=counter, column=1, pady=10)

            checkbox = CTkCheckBox(objFrame, text="", variable=friend.get("active"))
            checkbox.grid(row=counter, column=2, pady=10)

            counter += 1

    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(str(width - 1) + "x" + str(height))


def save():
    with open(str(Path.home().joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "w",
              encoding="UTF-8") as f:
        for friend in all_friends:
            active = friend.get("active").get() == 1
            f.write(friend.get("name") + ";" + friend.get("custom_wish") + ";" + str(active) + os.linesep)


def reload():
    for i in range(len(objFrame.winfo_children())):
        if i >= 1:
            objFrame.winfo_children()[1].destroy()
    root.update()
    browser = automation.ava_brauser()
    automation.logi_sisse(browser)
    friends = automation.sõbrad(browser)
    update_friends(friends)


def get_friends():
    driver = automation.ava_brauser()
    automation.logi_sisse(driver)
    return automation.sõbrad(driver)


def load_friends():
    global all_friends
    all_friends.clear()

    home = Path.home()
    path = home.joinpath("facebookBirthdayWisher", "pictures")
    path.mkdir(parents=True, exist_ok=True)  # if folder doesn't exist, create it

    image_files = Path(path).glob("*")

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        lines = f.readlines()
    non_empty_lines = []
    for line in lines:
        if line.strip():
            non_empty_lines.append(line)

    images = list(range(len(non_empty_lines)))

    for file in image_files:
        img = Image.open(file)
        img.resize((50, 50))
        photo_image = ImageTk.PhotoImage(img)
        images[int(file.name[3:-4])] = photo_image

        image_label = Label(objFrame, image=photo_image, background="#1E1E1E")
        image_label.grid(row=int(file.name[3:-4]) + 1, column=0, pady=10, padx=10)

    for i in range(len(non_empty_lines)):
        line_as_list = non_empty_lines[i].strip().split(';')

        checkbox_var = IntVar()
        if line_as_list[2] == "True":
            checkbox_var.set(1)

        all_friends.append({"image": images[i], "name": line_as_list[0], "custom_wish": line_as_list[1],
                            "active": checkbox_var})

        name_label = Label(objFrame, text=line_as_list[0], background="#1E1E1E", foreground="white")
        name_label.grid(row=i + 1, column=1, pady=10)

        checkbox = CTkCheckBox(objFrame, text="", variable=checkbox_var)
        checkbox.grid(row=i + 1, column=2, pady=10)

    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(str(width - 1) + "x" + str(height))


def update_friends(friend_list):
    global all_friends
    all_friends.clear()

    home = Path.home()
    home.joinpath("facebookBirthdayWisher", "pictures").mkdir(parents=True,
                                                              exist_ok=True)  # create folder to store images

    folder = str(home.joinpath("facebookBirthdayWisher", "pictures"))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        old_list = []

        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip() and len(line_as_list) == 3:
                old_list.append(
                    {"name": line_as_list[0], "custom_wish": line_as_list[1], "active": line_as_list[2] == "True"})

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "w", encoding="UTF-8") as f:

        for i in range(len(friend_list)):
            custom_wish = ""
            active = "False"
            for item in old_list:
                if friend_list[i].get("nimi") == item.get("name"):
                    # copy over active status and custom wish from old friend list
                    custom_wish = item.get("custom_wish")
                    if item.get("active"):
                        active = "True"

            f.write(friend_list[i].get("nimi") + ";" + str(custom_wish) + ";" + active + os.linesep)

            path = str(home.joinpath("facebookBirthdayWisher", "pictures")) + os.sep + "pic" + str(i) + ".jpg"
            urllib.request.urlretrieve(friend_list[i].get("pilt"), path)
            img = Image.open(path)
            img.resize((50, 50))
            photo_image = ImageTk.PhotoImage(img)

            checkbox_var = IntVar()
            if active == "True":
                checkbox_var.set(1)

            all_friends.append(
                {"image": photo_image, "name": friend_list[i].get("nimi"), "custom_wish": custom_wish,
                 "active": checkbox_var})

            image_label = Label(objFrame, image=photo_image, background="#1E1E1E")
            image_label.grid(row=i + 1, column=0, pady=10, padx=10)

            name_label = Label(objFrame, text=friend_list[i].get("nimi"), background="#1E1E1E", foreground="white")
            name_label.grid(row=i + 1, column=1, pady=10)

            checkbox = CTkCheckBox(objFrame, text="", variable=checkbox_var)
            checkbox.grid(row=i + 1, column=2, pady=10)

    root.update()
    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(str(width - 1) + "x" + str(height))


#  update frame layout after loading friends


set_appearance_mode("Dark")
set_default_color_theme("blue")

root = CTk()
root.geometry("750x580")
root.title("Facebooki automaatne õnnesoovija")
root.iconbitmap("Resources/icon.ico")
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

obj = ScrollableFrame(root, mousescroll=10)

objFrame = obj.frame

search_frame = Frame(objFrame, background="#1E1E1E", height=50, padx=50, pady=50)
search_frame.grid(row=0, column=0, columnspan=4, sticky="NW SE")

search_box = CTkEntry(search_frame, exportselection=False, bg_color="#1E1E1E", placeholder_text="Otsi sõpru", height=40,
                      width=200)
search_box.grid(row=0, column=0)
search_box.bind("<Return>", (lambda event: search()))

search_button = CTkButton(search_frame, width=40, height=40, text="Otsi", command=search)
search_button.grid(row=0, column=1, padx=5)

save_button = CTkButton(search_frame, width=40, height=40, text="Salvesta muudatused", command=save)
save_button.grid(row=0, column=2, padx=(100, 0))

reload_button = CTkButton(search_frame, width=40, height=40, text="Uuenda sõbralisti", command=reload)
reload_button.grid(row=0, column=3, padx=10)

all_friends = []

root.update()
load_friends()
root.mainloop()
