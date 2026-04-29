from flask import Flask, request, render_template_string, redirect, make_response, session
from markupsafe import escape
import sqlite3
import os
import secrets

app = Flask(__name__)
# было: app.secret_key = 'insecure-secret-key'
# стало: безопасная генерация ключа
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE='Lax'
)

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    test_users = [('admin', 'admin123'), ('user', 'user123')]
    for username, password in test_users:
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                     (username, password))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

init_db()

@app.after_request
def set_security_headers(response):
    # было: заголовки безопасности отсутствовали
    # стало: добавлены необходимые заголовки
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
def index():
    return '''
    <h1>Vulnerable DAST Demo App</h1>
    <p>Пример уязвимого приложения для лабораторной по DAST.</p>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (зависит от cookie)</a></li>
      <li><a href="/admin">Админка без нормальной авторизации</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>
    '''

@app.route('/echo')
def echo():
    # было: msg = request.args.get('msg', '')
    #       return f'<p>Вы ввели: {msg}</p>'  # уязвимо к XSS
    # стало: экранирование ввода через escape()
    msg = request.args.get('msg', '')
    safe_msg = escape(msg)
    return render_template_string(f'''
    <h2>Reflected Echo</h2>
    <p>Вы ввели: {safe_msg}</p>
    <a href="/">Назад</a>
    ''')

@app.route('/search')
def search():
    # было: query = f"SELECT * FROM users WHERE username = '{username}'"
    #       c.execute(query)  # уязвимо к SQL injection
    # стало: параметризованный запрос
    username = request.args.get('username', '')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    results = c.fetchall()
    conn.close()
    output = '<h2>Результаты поиска:</h2><ul>'
    for row in results:
        output += f'<li>ID: {escape(row[0])}, Username: {escape(row[1])}</li>'
    output += '</ul>'
    if not results:
        output += '<p>Пользователь не найден</p>'
    return output + '<a href="/">Назад</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # было: SQL-запрос через конкатенацию + роль в клиентской cookie
    # стало: параметризованный запрос + серверная сессия
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", 
                 (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/profile')
        return '<p style="color:red">Неверные данные</p><a href="/login">Назад</a>'
    return '''
    <h2>Вход</h2>
    <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password" type="password"><br>
        <input type="submit" value="Войти">
    </form>
    <a href="/">Назад</a>
    '''

@app.route('/profile')
def profile():
    # было: проверка роли из неподписанной cookie
    # стало: проверка через серверную сессию
    if 'user_id' not in session:
        return '<p>Требуется вход</p><a href="/login">Войти</a>'
    role = session.get('role', 'user')
    if role == 'admin':
        return '<h2>Профиль администратора</h2><p>Доступ разрешён!</p><a href="/">Назад</a>'
    return f'<h2>Профиль пользователя</h2><p>Ваша роль: {escape(role)}</p><a href="/">Назад</a>'

@app.route('/admin')
def admin():
    # было: if request.cookies.get('role') != 'admin':  # легко подделать
    # стало: проверка через серверную сессию
    if 'user_id' not in session or session.get('role') != 'admin':
        return '<p style="color:red">Доступ запрещён</p><a href="/">Назад</a>', 403
    return '<h2>Админ-панель</h2><p>Критические настройки системы</p><a href="/">Назад</a>'

@app.route('/files/')
def files_list():
    # было: os.listdir('vulnerable-app/files') — неверный путь в контейнере
    # стало: корректный путь относительно __file__
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(base_dir, 'files')
    if not os.path.exists(files_dir):
        return '<p>Директория файлов не найдена</p><a href="/">Назад</a>', 500
    files = [f for f in os.listdir(files_dir) if os.path.isfile(os.path.join(files_dir, f))]
    file_list = ''.join([f'<li><a href="/files/{escape(f)}">{escape(f)}</a></li>' for f in files])
    return f'<h2>Файлы</h2><ul>{file_list}</ul><a href="/">Назад</a>'

@app.route('/files/<filename>')
def serve_file(filename):
    # было: прямой доступ к файлу без проверки пути
    # стало: проверка, что файл существует и находится в разрешённой директории
    base_dir = os.path.dirname(os.path.abspath(__file__))
    files_dir = os.path.join(base_dir, 'files')
    filepath = os.path.join(files_dir, filename)
    # защита от path traversal
    if not os.path.abspath(filepath).startswith(os.path.abspath(files_dir)):
        return '<p>Доступ запрещён</p><a href="/files/">Назад</a>', 403
    if not os.path.exists(filepath):
        return '<p>Файл не найден</p><a href="/files/">Назад</a>', 404
    with open(filepath, 'r') as f:
        content = escape(f.read())
    return f'<pre>{content}</pre><a href="/files/">Назад</a>'

# было: app.run(debug=True) — опасно в продакшене
# стало: debug=False по умолчанию, можно переключить через окружение
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=8080, debug=debug_mode)