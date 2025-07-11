import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import json

FLASK_URL = "http://localhost:5000"
DJANGO_API_URL = "https://backend-ev66.onrender.com/api"

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

# Hàm gọi lấy thông tin user hiện tại Django (theo token)
def call_django_user():
    token = entry_token.get().strip()
    if not token:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập Token!")
        return
    headers = {'Authorization': f'Token {token}'}
    try:
        r = requests.get(f"{DJANGO_API_URL}/user/", headers=headers, timeout=10)  # Thêm timeout
        r.raise_for_status()
        res = r.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(res, indent=2))
    except requests.exceptions.HTTPError as e:
        messagebox.showerror("Lỗi", f"Lỗi HTTP khi gọi /user/: {str(e)} (Kiểm tra token hoặc endpoint)")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Lỗi kết nối đến Django API: {str(e)} (Kiểm tra mạng hoặc URL)")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}")

# Hàm gọi lấy user theo ID Django (theo token)
def call_django_user_by_id():
    user_id = entry_id.get().strip()
    token = entry_token.get().strip()
    if not user_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập User ID!")
        return
    if not token:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập Token!")
        return
    headers = {'Authorization': f'Token {token}'}
    try:
        r = requests.get(f"{DJANGO_API_URL}/user_by_id/?id={user_id}", headers=headers, timeout=10)  # Thêm timeout
        r.raise_for_status()
        res = r.json()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, json.dumps(res, indent=2))
    except requests.exceptions.HTTPError as e:
        messagebox.showerror("Lỗi", f"Lỗi HTTP khi gọi /user_by_id/: {str(e)} (Kiểm tra token, ID hoặc endpoint)")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Lỗi kết nối đến Django API: {str(e)} (Kiểm tra mạng hoặc URL)")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi không xác định: {str(e)}")

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

# Token nhập cho Django API
tk.Label(root, text="Nhập Token Django API:", anchor='w').pack(fill='x', padx=10)
entry_token = tk.Entry(root, width=80, show="*")
entry_token.pack(padx=10, pady=5)

btn_django_user = tk.Button(root, text="Lấy user hiện tại Django", command=call_django_user)
btn_django_user.pack(pady=5)

btn_django_user_by_id = tk.Button(root, text="Lấy user theo ID Django", command=call_django_user_by_id)
btn_django_user_by_id.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, width=80, height=30)
text_area.pack(padx=10, pady=10)

root.mainloop() #xóa phần thừa để khớp với from flask import Flask, request, jsonify
import sqlite3
import logging

app = Flask(__name__)
DB_PATH = 'demo.db'

# Cấu hình logging với mức độ có thể điều chỉnh
logging.basicConfig(level=logging.WARNING)  # Chỉ log WARNING và cao hơn, tắt INFO
# Nếu muốn bật lại logging, đổi thành: logging.basicConfig(level=logging.INFO)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            ip TEXT,
            time TEXT DEFAULT (datetime('now'))
        )
    ''')
    c.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (1, "admin"))
    c.execute('INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)', (2, "guest"))
    conn.commit()
    conn.close()

# Endpoint an toàn - tránh SQL Injection
@app.route('/user_safe')
def user_safe():
    user_id = request.args.get('id', '').strip()
    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Invalid id, please enter a positive integer"}), 400
    user_id = int(user_id)
    if user_id <= 0:
        return jsonify({"error": "Invalid id, please enter a positive integer"}), 400
    query = "SELECT username FROM users WHERE id = ?"
    log_query = f"SELECT username FROM users WHERE id = {user_id}"
    # Chỉ log nếu cần, ví dụ: logging.info(...) có thể bỏ hoặc điều kiện hóa
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Bỏ dòng log vào bảng logs nếu không muốn
        # c.execute("INSERT INTO logs (query, ip) VALUES (?, ?)", (log_query, request.remote_addr))
        # conn.commit()
        c.execute(query, (user_id,))
        row = c.fetchone()
        if row:
            return jsonify({"username": row[0]})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

# Endpoint không an toàn - dễ bị SQL Injection
@app.route('/user_unsafe')
def user_unsafe():
    user_id = request.args.get('id', '').strip()
    log_query = f"SELECT username FROM users WHERE id = {user_id}"
    # Chỉ log nếu cần, ví dụ: logging.info(...) có thể bỏ
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Bỏ dòng log vào bảng logs nếu không muốn
        # c.execute("INSERT INTO logs (query, ip) VALUES (?, ?)", (log_query, request.remote_addr))
        # conn.commit()
        query = f"SELECT username FROM users WHERE id = {user_id}"
        c.execute(query)
        rows = c.fetchmany(10)
        if rows:
            usernames = [row[0] for row in rows]
            return jsonify({"username": usernames})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Endpoint an toàn để lấy tất cả users
@app.route('/users', methods=['GET'])
def get_users():
    # Chỉ log nếu cần, ví dụ: logging.info(...) có thể bỏ
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        # Bỏ dòng log vào bảng logs nếu không muốn
        # log_query = "SELECT id, username FROM users"
        # c.execute("INSERT INTO logs (query, ip) VALUES (?, ?)", (log_query, request.remote_addr))
        # conn.commit()
        c.execute("SELECT id, username FROM users")
        rows = c.fetchall()
        if rows:
            users = [{"id": row[0], "username": row[1]} for row in rows]
            return jsonify(users)
        return jsonify({"error": "No users found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

# Xem log dưới dạng JSON (có thể tắt nếu không cần)
@app.route('/logs')
def get_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("SELECT id, query, ip, time FROM logs ORDER BY id DESC LIMIT 50")
        rows = c.fetchall()
        logs = [{"id": r[0], "query": r[1], "ip": r[2], "time": r[3]} for r in rows]
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(port=5000)