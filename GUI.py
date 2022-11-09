
from customtkinter import *

set_appearance_mode("Dark")
set_default_color_theme("blue")

root = CTk()
root.geometry("400x580")
root.title("Facebooki automaatne õnnesoovija")
root.iconbitmap("Resources/icon.ico")

nimed = []


def vajutus(*Args):
    global nimed
    label2 = CTkLabel(root, text=entry1.get())
    nimed += [entry1.get()]
    entry1.delete(0, END)
    label2.pack()
    return nimed


label1 = CTkLabel(text="Sisestage nimed, kellele soovite õnne soovida:")
entry1 = CTkEntry(placeholder_text="Otsi sõpru", )
button1 = CTkButton(root, text="Nime salvestamiseks vajutage", command=vajutus)


label1.pack()
entry1.pack()
button1.pack(pady=5)

entry1.bind("<Return>", vajutus)


root.mainloop()

