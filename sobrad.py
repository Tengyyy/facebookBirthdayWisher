import urllib.request

from tkinter import *
from customtkinter import *

from PIL import Image, ImageTk
from pathlib import Path

import automation
from ScrollableFrame import ScrollableFrame


def search_test():
    print(search_box.get())
    search_box.delete(0, "end")


def test():
    print("\n Active friends:")
    for friend in all_friends:
        if friend.get("active").get() == 1:
            print(friend.get("name"))


def get_friends():
    driver = automation.ava_brauser()
    automation.logi_sisse(driver)
    return automation.sõbrad(driver)


def load_friends():
    global all_friends, checkboxes
    all_friends.clear()
    checkboxes.clear()

    home = Path.home()
    path = home.joinpath("facebookBirthdayWisher", "pictures")
    path.mkdir(parents=True, exist_ok=True)  # if folder doesn't exist, create it

    image_files = Path(path).glob("*")

    images = []

    for file in image_files:
        img = Image.open(file)
        img.resize((50, 50))
        photo_image = ImageTk.PhotoImage(img)
        images.append(photo_image)

        image_label = Label(objFrame, image=photo_image)
        image_label.grid(row=int(file.name[3:-4]) + 1, column=0, pady=10, padx=10)

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        lines = f.read().splitlines()
        for i in range(len(lines)):
            line_as_list = lines[i].strip().split(';')
            checkbox_var = IntVar()
            if line_as_list[2] == "True":
                checkbox_var.set(1)
            checkboxes.append(checkbox_var)
            all_friends.append({"image": images[i], "name": line_as_list[0], "custom_wish": line_as_list[1],
                                "active": checkbox_var})

    for i in range(len(all_friends)):
        name_label = Label(objFrame, text=all_friends[i].get("name"))
        name_label.grid(row=i + 1, column=1, pady=10)

        checkbox = CTkCheckBox(objFrame, text="", variable=checkboxes[i], command=test)
        checkbox.grid(row=i + 1, column=2, pady=10)


def update_friends(friend_list):
    global all_friends, checkboxes
    all_friends.clear()
    checkboxes.clear()

    home = Path.home()
    home.joinpath("facebookBirthdayWisher", "pictures").mkdir(parents=True,
                                                              exist_ok=True)  # create folder to store images

    with open(str(home.joinpath("facebookBirthdayWisher")) + os.sep + "friend_list.txt", "r", encoding="UTF-8") as f:
        old_list = []

        for line in f:
            line_as_list = line.strip().split(';')
            if line.strip():
                old_list.append(
                    {"name": line_as_list[0], "custom_wish": line_as_list[1], "active": line_as_list[2] == "True"})

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

            path = str(home.joinpath("facebookBirthdayWisher", "pictures")) + os.sep + "pic" + str(i) + ".jpg"
            urllib.request.urlretrieve(friend_list[i].get("pilt"), path)
            img = Image.open(path)
            img.resize((50, 50))
            photo_image = ImageTk.PhotoImage(img)

            all_friends.append(
                {"image": photo_image, "name": friend_list[i].get("nimi"), "custom_wish": custom_wish,
                 "active": active == "True"})

            image_label = Label(objFrame, image=photo_image)
            image_label.grid(row=i + 1, column=0, pady=10, padx=10)

            name_label = Label(objFrame, text=friend_list[i].get("nimi"))
            name_label.grid(row=i + 1, column=1, pady=10)

            checkbox = CTkCheckBox(objFrame)
            checkbox.grid(row=i + 1, column=2, pady=10)
            if active == "True":
                checkbox.select()


    root.update()


#  update frame layout after loading friends



set_appearance_mode("Dark")
set_default_color_theme("blue")

root = CTk()
root.geometry("600x580")
root.title("Facebooki automaatne õnnesoovija")
root.iconbitmap("Resources/icon.ico")
root.bind_all("<Button-1>", lambda event: event.widget.focus_set())

obj = ScrollableFrame(root, mousescroll=10)

objFrame = obj.frame

search_frame = Frame(objFrame, background="yellow", height=50, padx=50, pady=50)
search_frame.grid(row=0, column=0, columnspan=4, sticky="NW SE")

search_box = CTkEntry(search_frame, exportselection=False, bg_color="purple", placeholder_text="Otsi sõpru", height=40,
                      width=200)
search_box.grid(row=0, column=0)

search_button = CTkButton(search_frame, width=40, height=40, text="", command=search_test)
search_button.grid(row=0, column=1)

save_button = CTkButton(search_frame, width=40, height=40, text="")
save_button.grid(row=0, column=2, padx=(150, 0))

reload_button = CTkButton(search_frame, width=40, height=40, text="")
reload_button.grid(row=0, column=3, padx=10)

all_friends = []
checkboxes = []

root.update()
load_friends()
root.mainloop()
