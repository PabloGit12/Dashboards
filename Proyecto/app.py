from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbticket'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)


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

@app.route('/consultas')
def consultas():
    return render_template('Consultas.html')

@app.route('/jefe')
def jefe():
    return render_template('Jefe.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        usuario = request.form['txtdepartamento']
        contraseña = request.form['txtcontraseña']
        cur = mysql.connection.cursor()
        cur.execute("SELECT departamento, contraseña FROM user WHERE departamento = %s AND contraseña = %s", (usuario, contraseña))
        usuario_encontrado = cur.fetchone()
        cur.close()
        if usuario_encontrado:
            departamento_encontrado = usuario_encontrado[0]  # Obtener el departamento
            contraseña_encontrada = usuario_encontrado[1]  # Obtener la contraseña

            # Verificar el departamento y la contraseña del usuario encontrado
            if departamento_encontrado == "jefe" and contraseña_encontrada == "jefe1234":
                # Si es jefe, redirigir a la página de jefe
                return redirect(url_for('jefe'))
            else:
                # Si no es jefe, redirigir a la página de cliente
                return redirect(url_for('cliente'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('index'))

@app.route('/procesar_solicitud', methods=['POST'])
def procesar_solicitud():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_soporte = request.form['tipo_soporte']
        detalles = request.form['detalles']
        fecha = request.form['fecha']
        departamento = request.form['departamento']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO solicitudes (nombre, tipo_soporte, detalles, fecha, departamento) VALUES (%s, %s, %s, %s, %s)", (nombre, tipo_soporte, detalles, fecha, departamento))
        mysql.connection.commit()
        cur.close()
        flash('Solicitud enviada correctamente')
        return redirect(url_for('consultas'))
    
@app.route('/consulta_tickets', methods=['GET'])
def consulta_tickets():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solicitudes")
    solicitudes = cur.fetchall()
    cur.close()
    return render_template('consultas.html', solicitudes=solicitudes)

from flask import jsonify

@app.route('/solicitudes', methods=['GET'])
def obtener_solicitudes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM solicitudes")
    solicitudes = cur.fetchall()
    cur.close()

    # Formatear los datos como una lista de objetos JSON
    solicitudes_formateadas = []
    for solicitud in solicitudes:
        solicitud_formateada = {
            'id': solicitud[0],
            'nombre': solicitud[1],
            'tipo_soporte': solicitud[2],
            'fecha': solicitud[3],
            'departamento': solicitud[4],
            'detalles': solicitud[5]
        }
        solicitudes_formateadas.append(solicitud_formateada)

    return jsonify(solicitudes_formateadas)
@app.route('/departamentos')
def departamentos():
    return render_template('Departamentos.html')


@app.route('/guardar_departamentos', methods=['POST'])
def guardar_departamento():
    if request.method == 'POST':
        nombre = request.form['nombre']
        responsable = request.form['responsable']
        
        # Aquí puedes realizar cualquier operación de guardado en la base de datos
        # por ejemplo, guardar en una base de datos SQL, en MongoDB, etc.
        
        # Por ahora, simplemente imprimiremos los datos recibidos para propósitos de demostración
        print("Nombre del departamento:", nombre)
        print("Responsable:", responsable)
        
        # Aquí puedes redirigir a una página de confirmación o renderizar una plantilla específica
        return '¡Departamento registrado con éxito!'
    else:
        return 'Error: método de solicitud no válido'
    

@app.route('/reportes')
def reportes():
    return render_template('Reportes.html')




if __name__ == '__main__':
    app.run(port=5000, debug=True)