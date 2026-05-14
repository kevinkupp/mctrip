import tkinter as tk

class Score:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.points = 0

        # Score ekraanile
        self.display = self.canvas.create_text(
            50, 30,
            text=f"Score: {self.points}",
            fill="white",
            font=("Arial", 24, "bold"),
            anchor="nw"
        )
        self.update_score()

    def update_score(self):
        self.points += 1
        self.canvas.itemconfig(self.display, text=f"Score: {self.points}")
        self.root.after(1000, self.update_score)