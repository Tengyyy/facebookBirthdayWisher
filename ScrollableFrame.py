from tkinter import *


class ScrollableFrame:
    """A scrollable tkinter frame that will fill the whole window"""

    def __init__(self, master, mousescroll=0):
        self.mousescroll = mousescroll
        self.master = master
        self.main_frame = Frame(self.master)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.main_frame, background="#1E1E1E")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.main_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.canvas_configure)

        self.frame = Frame(self.canvas, background="#1E1E1E")

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="frame")

        self.frame.bind("<Enter>", self.entered)
        self.frame.bind("<Leave>", self.left)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self, event):
        if self.mousescroll:
            self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def left(self, event):
        if self.mousescroll:
            self.canvas.unbind_all("<MouseWheel>")

    def canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.itemconfig("frame", width=self.canvas.winfo_width())
