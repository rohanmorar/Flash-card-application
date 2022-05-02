from tkinter import *
import pandas as pd
import random
timer = None
curr_card = {}
words_to_learn = {}

BACKGROUND_COLOR = "#B1DDC6"
SCALE_WIDTH = 800
SCALE_HEGHT = 526

# import data into [{frenchw1:engw1},...] format
try:
    DataFrame = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = DataFrame.to_dict(orient="records")

def flip_card():
    canvas.itemconfigure(title, text = "English", fill="white")
    canvas.itemconfigure(card_word, text = curr_card["English"], fill = "white")
    canvas.itemconfigure(card_background, image = back_img_png)

def gen_fr_word():
    global curr_card, flip_timer
    window.after_cancel(flip_timer)
    curr_card = random.choice(words_to_learn)
    canvas.itemconfigure(card_background, image = front_img_png)
    canvas.itemconfigure(title, text = "French", fill = "black")
    canvas.itemconfigure(card_word, text = curr_card["French"], fill = "black")
    flip_timer = window.after(3000, func= flip_card)

def know_card():
    words_to_learn.remove(curr_card)
    data = pd.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    gen_fr_word()
    print(len(words_to_learn))

window = Tk()
window.title("Quick-Lang")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)

flip_timer = window.after(3000, func= flip_card)

canvas = Canvas(width = 800, height = 526, bg = BACKGROUND_COLOR, highlightthickness = 0)

front_img_png = PhotoImage(file = "images/card_front.png")
back_img_png = PhotoImage(file = "images/card_back.png")
card_background = canvas.create_image(400, 263, image = front_img_png)
title = canvas.create_text(400,160, text = "Title", fill="black", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400,263, text = "word", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column = 0, row = 0, columnspan = 2)

r_img = PhotoImage(file="images/right.png")
right_button = Button(image=r_img, highlightthickness=0, bg= BACKGROUND_COLOR, bd = 0, command=know_card)
right_button.grid(column=1, row=1)

w_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=w_img, highlightthickness=0,  bg= BACKGROUND_COLOR, bd = 0,command =gen_fr_word)
wrong_button.grid(column=0, row=1)

gen_fr_word()

window.mainloop()