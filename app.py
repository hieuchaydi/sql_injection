from flask import Flask, request, jsonify
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