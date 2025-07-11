import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json

FLASK_URL = "http://localhost:5000"

def call_safe():
    user_id = entry_id.get().strip()
    if not user_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập User ID!")
        return
    if not user_id.isdigit() or int(user_id) <= 0:
        messagebox.showerror("Lỗi", "User ID phải là số nguyên dương hợp lệ!")
        return
    try:
        r = requests.get(f"{FLASK_URL}/user_safe", params={'id': user_id})
        r.raise_for_status()
        res = r.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(res, indent=2))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi gọi /user_safe: {str(e)}")

def call_unsafe():
    user_id = entry_id.get().strip()
    if not user_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập User ID!")
        return
    try:
        r = requests.get(f"{FLASK_URL}/user_unsafe", params={'id': user_id})
        r.raise_for_status()
        res = r.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(res, indent=2))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi gọi /user_unsafe: {str(e)}")

def load_logs():
    try:
        r = requests.get(f"{FLASK_URL}/logs")
        r.raise_for_status()
        logs = r.json()
        text_area.delete(1.0, tk.END)
        for log in logs:
            text_area.insert(tk.END, f"{log['time']} | {log['ip']} | {log['query']}\n")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi gọi /logs: {str(e)}")

def get_all_users():
    try:
        r = requests.get(f"{FLASK_URL}/users")
        r.raise_for_status()
        res = r.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(res, indent=2))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi gọi /users: {str(e)}")

root = tk.Tk()
root.title("SQL Injection Demo Client")

tk.Label(root, text="Nhập User ID (số nguyên dương cho /user_safe, bất kỳ cho /user_unsafe để thử SQL Injection)\nHoặc dùng /users để xem tất cả users an toàn", wraplength=300).pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="User ID:").pack(side=tk.LEFT)
entry_id = tk.Entry(frame, width=20)
entry_id.pack(side=tk.LEFT, padx=5)

btn_safe = tk.Button(frame, text="Gọi /user_safe (An toàn)", command=call_safe)
btn_safe.pack(side=tk.LEFT, padx=5)

btn_unsafe = tk.Button(frame, text="Gọi /user_unsafe (Không an toàn)", command=call_unsafe)
btn_unsafe.pack(side=tk.LEFT, padx=5)

btn_users = tk.Button(frame, text="Xem tất cả users (An toàn)", command=get_all_users)
btn_users.pack(side=tk.LEFT, padx=5)

btn_logs = tk.Button(frame, text="Xem logs", command=load_logs)
btn_logs.pack(side=tk.LEFT, padx=5)

text_area = scrolledtext.ScrolledText(root, width=80, height=30)
text_area.pack(padx=10, pady=10)

root.mainloop()