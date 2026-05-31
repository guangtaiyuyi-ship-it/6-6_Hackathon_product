import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import todo_store
from screensaver import ScreensaverWindow


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TODO スクリーンセイバー")
        self.geometry("600x650")
        self.configure(bg="#f5f5f5")

        entry_frame = tk.Frame(self, bg="#f5f5f5")
        entry_frame.pack(pady=20, fill="x", padx=20)

        self.todo_entry = tk.Entry(
            entry_frame, font=("Helvetica", 14), bd=2, relief="groove"
        )
        self.todo_entry.pack(side="left", fill="x", expand=True, ipady=4)

        self.deadline_options = {
            "今日が締切": (datetime.now()).strftime("%Y-%m-%d"),
            "1日後（明日）": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "2日後": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "3日以上先 / なし": "",
        }

        self.selected_deadline_label = tk.StringVar(value="3日以上先 / なし")
        deadline_menu = tk.OptionMenu(
            entry_frame, self.selected_deadline_label, *self.deadline_options.keys()
        )
        deadline_menu.config(font=("Helvetica", 10), bg="white")
        deadline_menu.pack(side="left", padx=5)

        self.categories = ["🛒 スーパー（食材）", "🧼 日用品・雑貨", "✨ 欲しいもの・その他"]
        self.selected_category = tk.StringVar(value="🛒 スーパー（食材）")
        category_menu = tk.OptionMenu(entry_frame, self.selected_category, *self.categories)
        category_menu.config(font=("Helvetica", 10), bg="white")
        category_menu.pack(side="left", padx=5)

        add_button = tk.Button(
            entry_frame,
            text="追加",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            bd=0,
            padx=15,
            command=self.on_add_click,
        )
        add_button.pack(side="right", padx=5)

        list_label = tk.Label(
            self,
            text="買うものリスト (売り場ごとに表示されます)",
            font=("Helvetica", 10, "bold"),
            bg="#f5f5f5",
            fg="#555",
        )
        list_label.pack(anchor="w", padx=20)

        self.canvas = tk.Canvas(self, bg="white", bd=2, relief="sunken")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True, padx=20, pady=5)
        scrollbar.pack(side="right", fill="y")

        slider_frame = tk.Frame(self, bg="#f5f5f5")
        slider_frame.pack(fill="x", padx=20, pady=15) 

        slider_label = tk.Label(
            slider_frame, text="全体の基本速度:", font=("Helvetica", 10), bg="#f5f5f5"
        )
        slider_label.pack(side="left")

        self.speed_slider = tk.Scale(
            slider_frame,
            from_=0.5,
            to=3.0,
            resolution=0.1,
            orient="horizontal",
            bg="#f5f5f5",
            bd=0,
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack(side="right", fill="x", expand=True, padx=10)

        self.start_button = tk.Button(
            self,
            text="スクリーンセイバー起動",
            font=("Helvetica", 14, "bold"),
            bg="#2196F3",
            fg="white",
            bd=0,
            pady=10,
            command=self.on_start_click,
        )
        self.start_button.pack(fill="x", padx=20, pady=20)

        self.refresh_todo_list()

    def refresh_todo_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        todos = todo_store.load_todos()
        category_frames = {}

        for cat in self.categories:
            cat_clean = cat.split()[-1]  

            frame = tk.LabelFrame(
                self.scrollable_frame,
                text=cat,
                font=("Helvetica", 11, "bold"),
                bg="white",
                fg="#333",
                padx=10,
                pady=10,
            )
            frame.pack(fill="x", expand=True, padx=10, pady=10)
            category_frames[cat_clean] = frame

        for todo in todos:
            todo_id = todo["id"]
            is_completed = todo["completed"]
            deadline_str = todo.get("deadline", "")
            todo_cat = todo.get("category", "欲しいもの・その他")

            _, icon, alert_color, _ = todo_store.get_deadline_status(deadline_str)

            parent_frame = category_frames.get(todo_cat, category_frames["欲しいもの・その他"])
            row_frame = tk.Frame(parent_frame, bg="white", pady=4)
            row_frame.pack(fill="x", expand=True)
            var = tk.BooleanVar(value=is_completed)
            cb = tk.Checkbutton(
                row_frame,
                variable=var,
                bg="white",
                activebackground="white",
                command=lambda tid=todo_id: self.on_toggle_click(tid),
            )
            cb.pack(side="left", padx=5)
            text_font = (
                ("Helvetica", 12, "bold")
                if not is_completed
                else ("Helvetica", 12, "overstrike")
            )
            text_color = alert_color if not is_completed else "#888888"
            display_text = f"{icon} {todo['text']}"
            if deadline_str and not is_completed:
                if deadline_str == datetime.now().strftime("%Y-%m-%d"):
                    display_text += " (今日買う！)"
                else:
                    display_text += " (明日買う)"
            label = tk.Label(
                row_frame,
                text=display_text,
                font=text_font,
                fg=text_color,
                bg="white",
                anchor="w",
            )
            label.pack(side="left", fill="x", expand=True)

            del_btn = tk.Button(
                row_frame,
                text="✕",
                fg="#FF5252",
                bg="white",
                bd=0,
                activebackground="#ffebee",
                font=("Helvetica", 10, "bold"),
                command=lambda tid=todo_id: self.on_delete_click(tid),
            )
            del_btn.pack(side="right", padx=10)

    def on_add_click(self):
        text = self.todo_entry.get()
        if text.strip():
            selected_menu_text = self.selected_deadline_label.get()
            deadline_date_str = self.deadline_options[selected_menu_text]
            selected_cat_text = self.selected_category.get().split()[-1]
            todo_store.add_todo(text, deadline_date_str, selected_cat_text)
            self.todo_entry.delete(0, tk.END)
            self.refresh_todo_list()
        else:
            messagebox.showwarning("警告", "買うものを入力してください。")

    def on_toggle_click(self, todo_id):
        todo_store.toggle_todo(todo_id)
        self.refresh_todo_list()

    def on_delete_click(self, todo_id):
        todo_store.remove_todo(todo_id)
        self.refresh_todo_list()

    def on_start_click(self):
        speed = self.speed_slider.get()
        ScreensaverWindow(self, speed_modifier=speed)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
