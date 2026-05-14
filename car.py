import tkinter as tk

class Car:
    def __init__(self, canvas):
        self.canvas = canvas
        self.id = canvas.create_rectangle(300, 800, 340, 880, fill="red", outline="black")
        self.speed = 20

    def move_left(self, event):
        self.canvas.move(self.id, -self.speed, 0)

    def move_right(self, event):
        self.canvas.move(self.id, self.speed, 0)