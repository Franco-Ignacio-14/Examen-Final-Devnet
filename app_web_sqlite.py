from flask import Flask, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "usuarios.db"

# Crear base de datos y tabla
def crear_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Insertar usuarios iniciales
def insertar_usuarios():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    usuarios = [
        ("Franco Retamales", generate_password_hash("devnet123")),
        ("admin", generate_password_hash("admin123"))
    ]

    for u in usuarios:
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (u[0],))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (?, ?)", u
            )

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM usuarios WHERE usuario = ?", (usuario,)
        )
        resultado = cursor.fetchone()
        conn.close()

        if resultado and check_password_hash(resultado[0], password):
            return f"<h2>Bienvenido {usuario}</h2>"
        else:
            return "<h2>Usuario o contraseña incorrectos</h2>"

    return """
        <h2>Login</h2>
        <form method="POST">
            Usuario: <input type="text" name="usuario"><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Ingresar">
        </form>
    """

if __name__ == "__main__":
    crear_db()
    insertar_usuarios()
    app.run(host="0.0.0.0", port=5800)
