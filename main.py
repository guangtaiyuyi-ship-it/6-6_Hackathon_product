import tkinter as tk
from tkinter import messagebox
import todo_store
from screensaver import ScreensaverWindow


class TodoApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("TODO スクリーンセイバー")
        self.geometry("500x600")
        self.configure(bg="#f5f5f5")

        entry_frame = tk.Frame(self, bg="#f5f5f5")
        entry_frame.pack(pady=20, fill="x", padx=20)  

        self.todo_entry = tk.Entry(
            entry_frame, font=("Helvetica", 14), bd=2, relief="groove"
        )
        self.todo_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.todo_entry.bind(
            "<Return>", lambda event: self.on_add_click()
        ) 

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
        add_button.pack(side="right", padx=10)  

        list_label = tk.Label(
            self,
            text="タスク一覧 (チェックで完了/未完了の切り替え)",
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

        self.canvas.pack(
            side="top", fill="both", expand=True, padx=20, pady=5
        )  
        scrollbar.pack(side="right", fill="y")

        slider_frame = tk.Frame(self, bg="#f5f5f5")
        slider_frame.pack(fill="x", padx=20, pady=15)  

        slider_label = tk.Label(
            slider_frame,
            text="スクリーンセイバーの速度:",
            font=("Helvetica", 10),
            bg="#f5f5f5",
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
        self.speed_slider.pack(
            side="right", fill="x", expand=True, padx=10
        ) 

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
        """データ層から最新のTODOを取得し、画面のチェックリストを再描画する"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        todos = todo_store.load_todos()

        for todo in todos:
            todo_id = todo["id"]
            is_completed = todo["completed"]

            row_frame = tk.Frame(self.scrollable_frame, bg="white", pady=2)
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

            text_font = ("Helvetica", 12)
            text_color = "black"
            if is_completed:
                text_font = ("Helvetica", 12, "overstrike")
                text_color = "#888888"

            label = tk.Label(
                row_frame,
                text=todo["text"],
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
            todo_store.add_todo(text)
            self.todo_entry.delete(0, tk.END)
            self.refresh_todo_list()
        else:
            messagebox.showwarning("警告", "タスクを入力してください。")

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
