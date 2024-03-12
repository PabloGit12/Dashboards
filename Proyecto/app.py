from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from xhtml2pdf import pisa
from io import BytesIO


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
    flash('Bienvenido')
    return render_template('index.html', consulta=consulta)

@app.route('/cliente')
def cliente():
    return render_template('cliente.html')

@app.route('/solicitud')
def solicitud():
    return render_template('Solicitud.html')

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
        departamento = request.form['departamento']
        tipo_soporte = request.form['tipo_soporte']
        detalles = request.form['detalles']
        fecha = request.form['fecha']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO solicitudes (nombre, departamento, tipo_soporte, detalles, fecha ) VALUES (%s, %s, %s, %s, %s)", (nombre, departamento, tipo_soporte, detalles, fecha ))
        mysql.connection.commit()
        cur.close()
        flash('Solicitud enviada correctamente')
        return redirect(url_for('consultas'))  # Redirigir a la ruta 'consultas' después de procesar la solicitud
    
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
            'departamento': solicitud[2],
            'tipo_soporte': solicitud[3],
            'detalles': solicitud[4],
            'fecha': solicitud[5]
            
            
        }
        solicitudes_formateadas.append(solicitud_formateada)

    return jsonify(solicitudes_formateadas)

@app.route('/departamentos')
def departamentos():
    return render_template('Departamentos.html')


@app.route('/guardar_departamentos', methods=['POST'])
def guardar_departamentos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        responsable = request.form['responsable']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO departamentos (nombre, responsable) VALUES (%s, %s)", (nombre, responsable))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('departamentos'))

@app.route('/editar_departamento/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        responsable = request.form['responsable']
        cur.execute("UPDATE departamentos SET nombre=%s, responsable=%s WHERE id=%s", (nombre, responsable, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('departamentos'))
    else:
        cur.execute("SELECT * FROM departamentos WHERE id = %s", [id])
        departamento = cur.fetchone()
        cur.close()
        return render_template('editar_departamento.html', departamento=departamento)

def obtener_departamentos_desde_bd():
    # Aquí podrías conectarte a tu base de datos y obtener los departamentos
    # Por ahora, simplemente retornaremos una lista de diccionarios como ejemplo
    return [
        {'id': 1, 'nombre': 'Departamento 1', 'responsable': 'Responsable 1'},
        {'id': 2, 'nombre': 'Departamento 2', 'responsable': 'Responsable 2'},
        {'id': 3, 'nombre': 'Departamento 3', 'responsable': 'Responsable 3'}
    ]
    
@app.route('/seeDepartamentos')
def seeDepartamentos():
    return render_template('seeDepartamentos.html')


@app.route('/eliminar_departamento/<int:id>')
def eliminar_departamento(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departamentos WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/reportes')
def reportes():
    return render_template('Reportes.html')

@app.route('/guardar_reporte', methods=['POST'])
def guardar_reporte():
    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form['txtdepartamento']
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']

        # Insertar datos en la tabla "reportes"
        cur = mysql.connection.cursor()
        query = "INSERT INTO reportes (nombre, departamento, fecha, descripcion) VALUES (%s, %s, %s, %s)"
        values = (nombre, departamento, fecha, descripcion)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        flash('Reporte generado y guardado correctamente.')

    return redirect(url_for('reportes'))

@app.route('/ver_reportes')
def ver_reportes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reportes ORDER BY departamento")
    reportes = cur.fetchall()
    cur.close()
    return render_template('ver_reportes.html', reportes=reportes)

@app.route('/descargar_reporte_pdf')
def descargar_reporte_pdf():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reportes ORDER BY departamento")
    reportes = cur.fetchall()
    cur.close()

    rendered = render_template('ver_reportes.html', reportes=reportes)
    pdf = render_pdf(rendered)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reportes.pdf'

    return response

def render_pdf(html):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)
    return pdf.getvalue()


@app.route('/crear_usuarios')
def crear_usuarios():
    return render_template('crear_usuario.html')

@app.route('/usuarios')
def usuarios():
    return render_template('Usuarios.html')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        
        # Insertar el nuevo usuario en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
        mysql.connection.commit()
        cur.close()
        
        # Redirigir a la página de lista de usuarios después de crear el usuario
        return redirect(url_for('usuarios'))

@app.route('/editar_usuario/<int:id>')
def editar_usuario(id):
    # Aquí implementarías la lógica para editar un usuario en la base de datos
    return f'Editar usuario con ID {id}'

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    # Aquí implementarías la lógica para eliminar un usuario de la base de datos
    return f'Eliminar usuario con ID {id}'


if __name__ == '__main__':
    app.run(port=5000, debug=True)