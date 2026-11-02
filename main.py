import time
from turtle import *

name = input("What is your name")         # <-- change this (use a space between names)

screen = Screen()
screen.setup(800, 400)
screen.bgcolor("black")
hideturtle()

pen = Turtle()
pen.shape("circle")
pen.speed(0)
pen.width(6)
pen.penup()

# every letter: a list of strokes, each stroke a list of (x, y) points
# on a 0-to-1 grid (0,0 = bottom-left, 1,1 = top-right)
letters = {
    "A": [[(0, 0), (0.5, 1), (1, 0)], [(0.2, 0.4), (0.8, 0.4)]],
    "B": [[(0, 0), (0, 1), (0.7, 1), (1, 0.85), (1, 0.65), (0.7, 0.5), (0, 0.5)],
          [(0.7, 0.5), (1, 0.35), (1, 0.15), (0.7, 0), (0, 0)]],
    "C": [[(1, 0.85), (0.7, 1), (0.3, 1), (0, 0.8), (0, 0.2), (0.3, 0), (0.7, 0), (1, 0.15)]],
    "D": [[(0, 0), (0, 1), (0.6, 1), (1, 0.7), (1, 0.3), (0.6, 0), (0, 0)]],
    "E": [[(1, 1), (0, 1), (0, 0), (1, 0)], [(0, 0.5), (0.8, 0.5)]],
    "F": [[(1, 1), (0, 1), (0, 0)], [(0, 0.5), (0.8, 0.5)]],
    "G": [[(1, 0.85), (0.7, 1), (0.3, 1), (0, 0.8), (0, 0.2), (0.3, 0), (0.7, 0),
           (1, 0.2), (1, 0.45), (0.55, 0.45)]],
    "H": [[(0, 1), (0, 0)], [(1, 1), (1, 0)], [(0, 0.5), (1, 0.5)]],
    "I": [[(0.2, 1), (0.8, 1)], [(0.5, 1), (0.5, 0)], [(0.2, 0), (0.8, 0)]],
    "J": [[(0.2, 1), (1, 1)], [(0.7, 1), (0.7, 0.2), (0.5, 0), (0.2, 0), (0, 0.2)]],
    "K": [[(0, 1), (0, 0)], [(1, 1), (0, 0.4), (1, 0)]],
    "L": [[(0, 1), (0, 0), (1, 0)]],
    "M": [[(0, 0), (0, 1), (0.5, 0.4), (1, 1), (1, 0)]],
    "N": [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    "O": [[(0.3, 0), (0, 0.2), (0, 0.8), (0.3, 1), (0.7, 1), (1, 0.8), (1, 0.2), (0.7, 0), (0.3, 0)]],
    "P": [[(0, 0), (0, 1), (0.7, 1), (1, 0.85), (1, 0.65), (0.7, 0.5), (0, 0.5)]],
    "Q": [[(0.3, 0), (0, 0.2), (0, 0.8), (0.3, 1), (0.7, 1), (1, 0.8), (1, 0.2), (0.7, 0), (0.3, 0)],
          [(0.6, 0.3), (1, 0)]],
    "R": [[(0, 0), (0, 1), (0.7, 1), (1, 0.85), (1, 0.65), (0.7, 0.5), (0, 0.5)],
          [(0.5, 0.5), (1, 0)]],
    "S": [[(1, 0.9), (0.7, 1), (0.3, 1), (0, 0.85), (0, 0.65), (0.3, 0.5),
           (0.7, 0.5), (1, 0.35), (1, 0.15), (0.7, 0), (0.3, 0), (0, 0.1)]],
    "T": [[(0, 1), (1, 1)], [(0.5, 1), (0.5, 0)]],
    "U": [[(0, 1), (0, 0.2), (0.3, 0), (0.7, 0), (1, 0.2), (1, 1)]],
    "V": [[(0, 1), (0.5, 0), (1, 1)]],
    "W": [[(0, 1), (0.25, 0), (0.5, 0.6), (0.75, 0), (1, 1)]],
    "X": [[(0, 1), (1, 0)], [(1, 1), (0, 0)]],
    "Y": [[(0, 1), (0.5, 0.5), (1, 1)], [(0.5, 0.5), (0.5, 0)]],
    "Z": [[(0, 1), (1, 1), (0, 0), (1, 0)]],
}

colors = ["red", "orange", "yellow", "lime", "cyan", "magenta"]

# ---- split the name into words (each space starts a new line) ----
parts = name.upper().split(" ")
words = []
for p in parts:
    if len(p) > 0:
        words.append(p)

line_count = len(words)
longest = 0
for w in words:
    if len(w) > longest:
        longest = len(w)

# ---- auto-size: must fit the longest word across AND all lines down ----
W = 700 / (1.3 * longest - 0.3)
if W > 80:
    W = 80
H_ = W * 1.4
line_gap = H_ * 0.4
total_h = line_count * H_ + (line_count - 1) * line_gap
if total_h > 250:
    W = W * 250 / total_h
    H_ = W * 1.4
    line_gap = H_ * 0.4
    total_h = line_count * H_ + (line_count - 1) * line_gap

gap = W * 0.3
top_y = total_h / 2 + 15
color_i = 0

# ---- write each word on its own line ----
for line in range(line_count):
    word = words[line]
    count = len(word)
    total_w = count * W + (count - 1) * gap
    start_x = -total_w / 2
    base_y = top_y - H_ - line * (H_ + line_gap)

    for n in range(count):
        ch = word[n]
        ox = start_x + n * (W + gap)

        if ch in letters:
            pen.color(colors[color_i % len(colors)])
            color_i = color_i + 1

            for stroke in letters[ch]:
                pen.penup()
                pen.goto(ox + stroke[0][0] * W, base_y + stroke[0][1] * H_)
                pen.pendown()

                for k in range(1, len(stroke)):
                    x0 = ox + stroke[k - 1][0] * W
                    y0 = base_y + stroke[k - 1][1] * H_
                    x1 = ox + stroke[k][0] * W
                    y1 = base_y + stroke[k][1] * H_
                    for s in range(1, 9):
                        pen.goto(x0 + (x1 - x0) * s / 8, y0 + (y1 - y0) * s / 8)
                        time.sleep(0.01)

            time.sleep(0.2)

# ---- finale: rainbow underline under the whole name ----
line_w = longest * W + (longest - 1) * gap
under_y = top_y - total_h - 30
pen.penup()
pen.goto(-line_w / 2, under_y)
pen.pendown()
x = -line_w / 2
i = 0
while x < line_w / 2:
    pen.color(colors[i % len(colors)])
    x = x + 10
    pen.goto(x, under_y)
    time.sleep(0.01)
    i = i + 1

screen.mainloop()
