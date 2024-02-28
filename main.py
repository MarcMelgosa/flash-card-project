from tkinter import *

import pandas
from pandas import *
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data_save = pandas.DataFrame(to_learn)
    data_save.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, background=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
canvas.config(background=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right = Button(image=right_img, borderwidth=0, highlightthickness=0, command=is_known)
right.grid(column=1, row=1)

wrong_img = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_img, borderwidth=0, highlightthickness=0, command=next_card)
wrong.grid(column=0, row=1)

next_card()

window.mainloop()
