import tkinter as tk

# McTrip Window
class Background():
    root = tk.Tk()
    canvas = tk.Canvas(root, width=640, height=960, bg="gray", highlightthickness=0)
    canvas.pack()
    root.title("McTrip")
    root.geometry("640x960")
    
    # Background värv
    canvas.configure(background="gray")
    
    # Valged kastid keset teed
    squares = []
    for i in range(15):
        line = canvas.create_rectangle(315, i * 100, 325, i * 100 + 40, fill="white", outline="")
        squares.append(line)
    
    # Scroll funktsioon mis liigutab valgeid kaste
    def scroll():
        for s in squares:
            canvas.move(s, 0, 5) # Kiirus, mida suurem kolmas number seda kiirem on, max on 100
            if canvas.coords(s)[1] > 960:
                canvas.move(s, 0, -1500)
        root.after(10, scroll)
    scroll()
    
    #Lõpp
    root.mainloop()
