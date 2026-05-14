class Timer:
    def __init__(self, canvas, root):
        self.canvas = canvas
        self.root = root
        self.time = 0

        self.display = self.canvas.create_text(
            0, 0,
            text=f"Timer: {self.time}",
            fill="white",
            font=("Arial", 24, "bold"),
            anchor="ns"
        )
        self.update_timer()

    def update_timer(self):
        self.time += 1
        self.canvas.itemconfig(self.display, text=f"Timer: {self.time}")
        self.root.after(1000, self.update_timer)