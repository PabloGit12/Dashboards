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

    
@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vnombre = request.form['txtnombre']
        Vcontraseña = request.form['txtcontraseña']
        
        cs = mysql.connection.cursor()
        cs.execute('INSERT INTO user (nombre, contraseña) VALUES (%s, %s)', (Vnombre, Vcontraseña))
        mysql.connection.commit()
        
        flash('Inicio de sesión exitoso')
        return redirect(url_for('Cliente.html'))


@app.route('/solicitud')
def solicitud():
    return render_template('Solicitud.html')

@app.route('/consultas')
def consultas():
    return render_template('Consultas.html')

@app.route('/cliente')
def cliente():
    return render_template('Cliente.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
