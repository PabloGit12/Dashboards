from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbticket'
app.secret_key='mysecretkey'

mysql= MySQL(app)

@app.route('/')
def index():
    curSelect = mysql.connection.cursor()
    curSelect.execute('SELECT * FROM user')
    consulta = curSelect.fetchall()
    return render_template('index.html', consulta=consulta)

@app.route('/cliente')
def cliente():
    return render_template('cliente.html')

@app.route('/solicitud')
def solicitud():
    return render_template('solicitud.html')

    
@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        usuario = request.form['txtdepartamento']
        contraseña = request.form['txtcontraseña']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE departamento = %s AND contraseña = %s", (usuario, contraseña))
        usuario_encontrado = cur.fetchone()
        cur.close()
        if usuario_encontrado:
            return redirect(url_for('cliente'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/solicitud')
def solicitud():
    return render_template('Solicitud.html')

@app.route('/consultas')
def consultas():
    return render_template('Consultas.html')

@app.route('/cliente')
def cliente():
    return render_template('cliente.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
