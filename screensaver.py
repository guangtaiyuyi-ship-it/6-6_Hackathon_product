import tkinter as tk
import random
import todo_store 


class FloatingItem:

    def __init__(self, canvas, text, base_color, speed_multiplier):
        self.canvas = canvas
        self.text = text
        self.canvas_width = canvas.winfo_reqwidth()
        self.canvas_height = canvas.winfo_reqheight()

        x = random.randint(100, max(200, self.canvas_width - 100))
        y = random.randint(100, max(200, self.canvas_height - 100))

        self.id = canvas.create_text(
            x,
            y,
            text=self.text,
            fill=base_color,
            font=("Helvetica", 24, "bold"),
            anchor="nw",
        )
        self.color_list = [
            "#FF5733",
            "#33FF57",
            "#3357FF",
            "#F3FF33",
            "#FF33F3",
            "#33FFF0",
        ]
        base_dx = random.choice([-3, -2, 2, 3])
        base_dy = random.choice([-3, -2, 2, 3])
        self.dx = base_dx * speed_multiplier
        self.dy = base_dy * speed_multiplier

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
        all_todos = todo_store.load_todos()
        self.items = []
        for todo in all_todos:
            if not todo["completed"]:
                if hasattr(todo_store, "get_deadline_status"):
                    _, icon, color, item_speed_mult = todo_store.get_deadline_status(todo.get("deadline", ""))
                else:
                    icon, color, item_speed_mult = "✅", "#33FF57", 1.0
                category_tag = f"[{todo.get('category', 'その他')}] "
                display_text = f"{icon} {category_tag}{todo['text']}"

                item = FloatingItem(self.canvas, display_text, color, item_speed_mult)
                self.items.append(item)

        if not self.items:
            self.items = [FloatingItem(self.canvas, "🎉 すべてのタスクが完了しました！", "#33FF57", 1.0)]

        self.bind("<Escape>", self.close_screensaver) 
        self.bind("<Return>", self.close_screensaver)  
        self.bind("<space>", self.close_screensaver)   
        self.focus_set()
        self.animate()

    def animate(self):
        for item in self.items:
            item.update_position()
        interval = max(5, int(16 / self.speed_modifier))
        self.after(interval, self.animate)

    def close_screensaver(self, event=None):
        self.destroy()
