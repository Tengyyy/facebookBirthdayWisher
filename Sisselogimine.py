from tkinter import *
from customtkinter import *

set_appearance_mode("Dark")
set_default_color_theme("blue")

root = CTk()
root.geometry("400x580")
root.title("Sisselogija")
root.iconbitmap("icon.ico")


ls2 = []
f = open("andmed.txt", "r")
for i in f:
    ls2 += [i.strip()]
   
def vajutus():
    andmed = []
    andmed += [entry1.get()] #kasutajanimi
    andmed += [entry2.get()] #parool
    f = open("andmed.txt", "w")
    f.write(andmed[0] + "\n")
    f.write(andmed[1])
    f.close()
    return andmed

label0 = CTkLabel(root, text = "Palun logige ennast sisse:")
label1 = CTkLabel(root, text="Kasutajanimi: ")
label2 = CTkLabel(root, text="Parool: ")
entry1 = CTkEntry(root)
entry2 = CTkEntry(root, show="*")
entry1.insert(END, ls2[0])
entry2.insert(END, ls2[1])   
button1 = CTkButton(root, text="Logi sisse", command=lambda: [vajutus(), root.destroy()])

f.close()

label0.grid(row=1, column=2)
label1.grid(row=2,column=1)
label2.grid(row=3, column=1)
entry1.grid(row=2, column=2, pady=5)
entry2.grid(row=3, column=2)
button1.grid(row=4, column=2, pady=10)



root.mainloop()
