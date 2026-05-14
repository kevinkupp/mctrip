import tkinter as tk

class Game:
    # KONSTRUKTOR
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("McTrip")
        self.root.geometry("640x960")

        # Canvase tegemine
        self.canvas = tk.Canvas(self.root, width=640, height=960, bg="gray", highlightthickness=0)
        self.canvas.pack()

        # Valged teemärgistused
        self.squares = []
        for i in range(15):
            line = self.canvas.create_rectangle(315, i * 100, 325, i * 100 + 40, fill="white", outline="")
            self.squares.append(line)

        # Käivitab scroll meetodi
        self.scroll()
        self.root.mainloop()

    # Scroll funktsioon mis liigutab valged kaste
    def scroll(self):
        for s in self.squares:
            self.canvas.move(s, 0, 5) # Kiirus, mida suurem kolmas number seda kiirem on, max on 100
            if self.canvas.coords(s)[1] > 960:
                self.canvas.move(s, 0, -1500)
        self.root.after(10, self.scroll)

game = Game()