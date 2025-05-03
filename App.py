from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Crear base de datos y tablas
def crear_base():
    conn = sqlite3.connect('moda_verona.db')
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT,
        role TEXT,
        created_at TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT,
        phone TEXT,
        birthday DATE,
        style_profile TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    conn.commit()
    conn.close()

crear_base()

# Ruta para registrar cliente
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        birthday = request.form['birthday']  # Asegúrate de que esté en formato 'YYYY-MM-DD'
        style_profile = request.form['style_profile']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Convertir a cadena

        conn = sqlite3.connect('moda_verona.db')
        cursor = conn.cursor()

        # Insertar en users
        cursor.execute('INSERT INTO users (username, email, password, role, created_at) VALUES (?, ?, ?, ?, ?)',
                       (username, email, password, 'client', created_at))
        user_id = cursor.lastrowid

        # Insertar en clients
        cursor.execute('INSERT INTO clients (user_id, name, phone, birthday, style_profile, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, name, phone, birthday, style_profile, created_at))

        conn.commit()
        conn.close()

        return redirect('/clientes')

    return render_template('registro_cliente.html')

# Ruta para mostrar lista de clientes
@app.route('/clientes')
def clientes():
    conn = sqlite3.connect('moda_verona.db')
    cursor = conn.cursor()
    cursor.execute('SELECT users.username, users.email, clients.name, clients.phone, clients.birthday, clients.style_profile '
                   'FROM clients '
                   'JOIN users ON clients.user_id = users.id')

    clientes = cursor.fetchall()
    conn.close()
    return render_template('lista_clientes.html', clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True)
