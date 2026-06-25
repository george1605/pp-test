import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Forme geometrice")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.circle_btn = tk.Button(root, text="Deseneaza cerc", command=self.draw_circle)
        self.square_btn = tk.Button(root, text="Deseneaza patrat", command=self.draw_square)

        self.circle_btn.pack()
        self.square_btn.pack()

    def draw_circle(self):
        self.canvas.create_oval(100, 50, 200, 150, outline="blue", width=2)

    def draw_square(self):
        self.canvas.create_rectangle(220, 50, 320, 150, outline="red", width=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
