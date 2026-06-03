import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import todo_store
from screensaver import ScreensaverWindow


class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("買い物リストスクリーンセイバー")
        self.geometry("650x700")
        self.configure(bg="#f5f5f5")
        self.categories = ["🛒 スーパー","🧼 日用品・雑貨","✨ その他"]
        self.current_filter = tk.StringVar(value="すべて")

        entry_frame = tk.Frame(self, bg="#f5f5f5")
        entry_frame.pack(pady=(15, 5), fill="x", padx=20)
        self.todo_entry = tk.Entry(
            entry_frame, font=("Helvetica", 14), bd=2, relief="groove")
        self.todo_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.todo_entry.bind("<Return>", lambda event: self.on_add_click())

        self.deadline_options = {
            "今日買う": (datetime.now()).strftime("%Y-%m-%d"),
            "明日買う": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "今度でいい": "",
        }
        self.selected_deadline_label = tk.StringVar(value="今度でいい")
        deadline_menu = tk.OptionMenu(
            entry_frame, self.selected_deadline_label, *self.deadline_options.keys()
        )
        deadline_menu.config(font=("Helvetica", 10), bg="white")
        deadline_menu.pack(side="left", padx=5)

        self.categories = [
            "🛒 スーパー",
            "🧼 日用品・雑貨",
            "✨ その他",
        ]
        self.selected_category = tk.StringVar(value="🛒 スーパー")
        category_menu = tk.OptionMenu(
            entry_frame, self.selected_category, *self.categories
        )
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

        filter_frame = tk.Frame(self, bg="#e8e8e8", pady=2)
        filter_frame.pack(fill="x", padx=20, pady=5)

        filter_label = tk.Label(filter_frame, text="🔍 絞り込み:", font=("Helvetica", 10, "bold"), bg="#e8e8e8", fg="#555")
        filter_label.pack(side="left", padx=10, pady=5)

        filter_options = ["すべて"] + [cat.split()[-1] for cat in self.categories]
        for opt in filter_options:
            rb = tk.Radiobutton(
                filter_frame, text=opt, value=opt, variable=self.current_filter,
                indicatoron=False, font=("Helvetica", 10), bg="white", fg="#333",
                selectcolor="#2196F3", activebackground="#2196F3", bd=1, relief="raised",
                padx=10, command=self.refresh_todo_list 
            )
            rb.pack(side="left", padx=4, pady=5)

        list_label = tk.Label(
            self,
            text="買うものリスト (タスク名をダブルクリックでその場で編集できます)",
            font=("Helvetica", 10, "bold"),
            bg="#f5f5f5",
            fg="#555",
        )
        list_label.pack(anchor="w", padx=20, pady=(5,0))

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

        self.trash_frame = tk.LabelFrame(
            self,
            text="🗑️ ゴミ箱（一時削除）",
            font=("Helvetica", 11, "bold"),
            bg="#eeeeee",
            fg="#666",
            padx=10,
            pady=2,
        )
        self.trash_frame.pack(fill="x", padx=20, pady=10)

        clear_trash_btn = tk.Button(
            self.trash_frame,
            text="ゴミ箱を空にする",
            font=("Helvetica", 9),
            bg="#e0e0e0",
            fg="#333",
            bd=1,
            command=self.on_clear_trash_click,
        )
        clear_trash_btn.pack(anchor="e")

        self.trash_items_frame = tk.Frame(self.trash_frame, bg="#eeeeee")
        self.trash_items_frame.pack(fill="x", expand=True, pady=2)

        self.start_button = tk.Button(
            self,
            text="スクリーンセイバー起動",
            font=("Helvetica", 14, "bold"),
            bg="#2196F3",
            fg="white",
            bd=0,
            pady=10,
            command=self.on_start_click)
        self.start_button.pack(fill="x", padx=20, pady=(10, 25))

        self.refresh_todo_list()

    def refresh_todo_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.trash_items_frame.winfo_children():
            widget.destroy()

        todos = todo_store.load_todos()
        category_frames = {}
        active_filter = self.current_filter.get()

        for cat in self.categories:
            cat_clean = cat.split()[-1]
            if active_filter == "すべて" or active_filter == cat_clean:
                frame = tk.LabelFrame(self.scrollable_frame, text=cat, font=("Helvetica", 11, "bold"), bg="white", fg="#333", padx=10, pady=10)
                frame.pack(fill="x", expand=True, padx=10, pady=5)
                category_frames[cat_clean] = frame

        for todo in todos:
            todo_id = todo["id"]
            is_completed = todo["completed"]
            deadline_str = todo.get("deadline", "")
            todo_cat = todo.get("category", "その他")
            is_deleted = todo.get("deleted", False)

            if active_filter != "すべて" and active_filter != todo_cat:
                continue

            if is_deleted:
                row_frame = tk.Frame(self.trash_items_frame, bg="#eeeeee", pady=2)
                row_frame.pack(fill="x", expand=True)

                label = tk.Label(
                    row_frame,
                    text=f"[{todo_cat}] {todo['text']}",
                    font=("Helvetica", 11),
                    fg="#888888",
                    bg="#eeeeee",
                    anchor="w",
                )
                label.pack(side="left", fill="x", expand=True)

                restore_btn = tk.Button(
                    row_frame,
                    text="↩️ 復元",
                    fg="#2196F3",
                    bg="#eeeeee",
                    bd=0,
                    font=("Helvetica", 10, "bold"),
                    command=lambda tid=todo_id: self.on_restore_click(tid),
                )
                restore_btn.pack(side="right", padx=10)
                continue

            _, icon, alert_color, _ = todo_store.get_deadline_status(deadline_str)
            parent_frame = category_frames.get(todo_cat)

            if not parent_frame:
                continue

            row_frame = tk.Frame(parent_frame, bg="white", pady=4)
            row_frame.pack(fill="x", expand=True)

            cb = tk.Checkbutton(
                row_frame,
                bg="white",
                activebackground="white",
                variable=tk.BooleanVar(value=is_completed),
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

            if not is_completed:
                label.bind(
                    "<Double-1>",
                    lambda event, label_obj=label, tid=todo_id, current_val=todo[
                        "text"
                    ]: self.enable_inline_edit(label_obj, tid, current_val),
                )

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

    def enable_inline_edit(self, label_obj, todo_id, current_text):
        parent = label_obj.master
        label_obj.pack_forget()

        edit_entry = tk.Entry(parent, font=("Helvetica", 12), bd=1, relief="solid")
        edit_entry.insert(0, current_text)
        edit_entry.pack(side="left", fill="x", expand=True, padx=5)
        edit_entry.focus_set()

        edit_entry.bind(
            "<Return>", lambda e: self.save_inline_edit(edit_entry, todo_id)
        )
        edit_entry.bind(
            "<FocusOut>", lambda e: self.save_inline_edit(edit_entry, todo_id)
        )

    def save_inline_edit(self, entry_obj, todo_id):
        new_text = entry_obj.get()
        if new_text.strip():
            todo_store.update_todo_text(todo_id, new_text)

        entry_obj.destroy()
        self.refresh_todo_list()

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

    def on_restore_click(self, todo_id):
        todo_store.restore_todo(todo_id)
        self.refresh_todo_list()

    def on_clear_trash_click(self):
        if messagebox.askyesno(
            "確認", "ゴミ箱の中身を完全に消去しますか？（復元できなくなります）"
        ):
            todo_store.clear_trash()
            self.refresh_todo_list()

    def on_start_click(self):
        current_filter_val = self.current_filter.get()
        ScreensaverWindow(self, speed_modifier=1.0, current_filter=current_filter_val)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
