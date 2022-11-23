import urllib.request

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
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())


obj = ScrollableFrame(root, mousescroll=10)

objFrame = obj.frame

search_frame = Frame(objFrame, background="yellow", height=50, padx=50, pady=50)
search_frame.grid(row=0, column=0, columnspan=3, sticky="NW SE")

search_box = CTkEntry(search_frame, exportselection=False, bg_color="purple", placeholder_text="Otsi sõpru", height=40, width=200)
search_box.grid(row=0, column=0)

search_button = CTkButton(search_frame, width=40, height=40, text="")
search_button.grid(row=0, column=1)


displayed_friends = []  # keep track of friends that are currently visible on the screen, dictionary {"name": ******, "checkbox": ******}


def test():
    print("test")


def check_action(self, friend):  # pass checkbox as parameter
    for item in displayed_friends:
        if item[0] == friend:
            item[2] = self.value  # value of the checkbox

    for container in displayed_friends:
        if container.get("name") == friend and container.get("checkbox") != self:
            if self.value:
                container.get("checkbox").select()
            else:
                container.get("checkbox").deselect()


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
        image_label.grid(row=int(file.name[3:-4])+1, column=0, pady=10, padx=10)

    name_list = []
    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip():
                name_list.append({"name": line_as_list[0], "custom_wish": line_as_list[1], "active": line_as_list[2] == "True"})

    global displayed_friends
    displayed_friends.clear()

    for i in range(len(name_list)):
        name_label = Label(objFrame, text=name_list[i].get("name"))
        name_label.grid(row=i+1, column=1, pady=10)

        # use intvars for the checkboxes
        checkbox = CTkCheckBox(objFrame, text="", command=test)
        checkbox.grid(row=i+1, column=2, pady=10)
        if name_list[i].get("active"):
            print("su ema")
            checkbox.select()

        displayed_friends.append({"name": name_list[i].get("name"), "checkbox": checkbox})

    return name_list


def update_friends(friend_list):
    images.clear()
    home = Path.home()
    home.joinpath("facebookBirthdayWisher", "pictures").mkdir(parents=True,
                                                              exist_ok=True)  # create folder to store images

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        old_list = []

        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip():
                old_list.append({"name": line_as_list[0], "custom_wish": line_as_list[1], "active": line_as_list[2] == "True"})

    new_list = []

    global displayed_friends
    displayed_friends.clear()

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
            new_list.append({"name": friend_list[i].get("nimi"), "custom_wish": custom_wish, "active": active == "True"})

            path = str(home.joinpath("facebookBirthdayWisher", "pictures")) + os.sep + "pic" + str(i) + ".jpg"
            urllib.request.urlretrieve(friend_list[i].get("pilt"), path)
            img = Image.open(path)
            img.resize((50, 50))
            photo_image = ImageTk.PhotoImage(img)
            images.append(photo_image)

            image_label = Label(objFrame, image=photo_image)
            image_label.grid(row=i+1, column=0, pady=10, padx=10)

            name_label = Label(objFrame, text=friend_list[i].get("nimi"))
            name_label.grid(row=i+1, column=1, pady=10)

            checkbox = CTkCheckBox(objFrame)
            checkbox.grid(row=i+1, column=2, pady=10)
            if active == "True":
                checkbox.select()

            displayed_friends.append({"name": friend_list[i].get("nimi"), "checkbox": checkbox})

    root.update()
    return new_list


#  update frame layout after loading friends

root.update()
load_friends()
root.mainloop()
