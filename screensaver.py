import tkinter as tk
import random
from todo_store import load_todos


class FloatingItem:

    def __init__(self, canvas, text):
        self.canvas = canvas
        self.text = text

        self.canvas_width = canvas.winfo_reqwidth()
        self.canvas_height = canvas.winfo_reqheight()

        x = random.randint(100, max(200, self.canvas_width - 100))
        y = random.randint(100, max(200, self.canvas_height - 100))

        self.color_list = [
            "#FF5733",
            "#33FF57",
            "#3357FF",
            "#F3FF33",
            "#FF33F3",
            "#33FFF0",
        ]
        current_color = random.choice(self.color_list)

        self.id = canvas.create_text(
            x,
            y,
            text=self.text,
            fill=current_color,
            font=("Helvetica", 24, "bold"),
            anchor="nw",
        )

        self.dx = random.choice([-4, -3, 3, 4])
        self.dy = random.choice([-4, -3, 3, 4])

    def update_position(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if x1 + self.dx < 0 or x2 + self.dx > canvas_w:
            self.dx = -self.dx  
            self.change_color()  

        if y1 + self.dy < 0 or y2 + self.dy > canvas_h:
            self.dy = -self.dy  
            self.change_color()  

        self.canvas.move(self.id, self.dx, self.dy)

    def change_color(self):
        new_color = random.choice(self.color_list)
        self.canvas.itemconfig(self.id, fill=new_color)


class ScreensaverWindow(tk.Toplevel):
    def __init__(self, parent, speed_modifier=1.0):
        super().__init__(parent)
        self.speed_modifier = speed_modifier
        self.attributes("-fullscreen", True)
        self.configure(bg="black")
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        all_todos = load_todos()
        active_todos = [todo["text"] for todo in all_todos if not todo["completed"]]

        if not active_todos:
            active_todos = ["すべてのタスクが完了しました！", "素晴らしい一日を！"]

        self.items = [FloatingItem(self.canvas, text) for text in active_todos]
        self.bind("<Any-KeyPress>", self.close_screensaver)
        self.bind("<Motion>", self.close_screensaver)
        self.bind("<Button-1>", self.close_screensaver)
        self.animate()

    def animate(self):
        for item in self.items:
            item.update_position()
        interval = max(5, int(16 / self.speed_modifier))
        self.after(interval, self.animate)

    def close_screensaver(self, event=None):
        self.destroy()
