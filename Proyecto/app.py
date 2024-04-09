from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask import send_file
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter



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

@app.route('/auxiliar')
def auxiliar():
    return render_template('Auxiliar.html')

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

@app.route('/eliminar_ticket/<id>', methods=['POST'])
def eliminar_ticket(id):
    if request.method == 'POST':
        curEli = mysql.connection.cursor()
        curEli.execute('DELETE FROM tickets WHERE id=%s', (id,))
        mysql.connection.commit()
        flash('El ticket ha sido eliminado correctamente.')
    return redirect(url_for('consulta'))



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

    
@app.route('/seeDepartamentos')
def seeDepartamentos():
    return render_template('seeDepartamentos.html')

@app.route('/seedepartamentos')
def seesdepartamentos():
    # 1. Obtener los datos de los departamentos desde la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM departamentos")
    departamentos = cur.fetchall()
    cur.close()
    
    # 2. Pasar los datos de los departamentos a la plantilla 'seesDepartamentos.html'
    return render_template('seesDepartamentos.html', departamentos=departamentos)



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

        try:
            cur = mysql.connection.cursor()
            query = "INSERT INTO reportes (nombre, departamento, fecha, descripcion) VALUES (%s, %s, %s, %s)"
            values = (nombre, departamento, fecha, descripcion)
            cur.execute(query, values)
            mysql.connection.commit()
            cur.close()

            flash('Reporte generado y guardado correctamente.')
        except Exception as e:
            flash(f'Error al guardar el reporte: {str(e)}', 'error')

    return redirect(url_for('reportes'))

@app.route('/ver_reportes')
def ver_reportes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reportes ORDER BY departamento")
    reportes = cur.fetchall()
    cur.close()
    return render_template('ver_reportes.html', reportes=reportes)



@app.route('/descargar_reporte_pdf/<id>')
def descargar_reporte_pdf(id):
    # Aquí recuperarías los datos del reporte usando el ID proporcionado
    # Supongamos que tienes una función para obtener los datos del reporte desde la base de datos
    reporte = obtener_reporte_desde_bd(id)

    # Verificar si se encontró el reporte con el ID proporcionado
    if reporte:
        # Recuperar los datos del reporte
        nombre = reporte['nombre']
        departamento = reporte['departamento']
        fecha = reporte['fecha']
        descripcion = reporte['descripcion']

        # Crear el PDF utilizando ReportLab
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.drawString(100, 750, f"Nombre: {nombre}")
        c.drawString(100, 730, f"Departamento: {departamento}")
        c.drawString(100, 710, f"Fecha: {fecha}")
        c.drawString(100, 690, f"Descripción: {descripcion}")
        c.save()

        # Devolver el PDF generado como una respuesta para descargar
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, attachment_filename='reporte.pdf', mimetype='application/pdf')
    else:
        # Si no se encuentra el reporte, devolver un mensaje de error o redirigir a una página de error
        return 'Reporte no encontrado', 404
    

    
def obtener_reporte_desde_bd(id):
    # Aquí implementa la lógica para recuperar los datos del reporte desde la base de datos
    # Puedes utilizar Flask-MySQL para realizar consultas a la base de datos y recuperar los datos del reporte
    # Por ejemplo, si estás utilizando Flask-MySQL, podrías hacer algo como esto:
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reportes WHERE id = %s", [id])
    reporte = cur.fetchone()
    cur.close()
    
    # Verificar si se encontró el reporte con el ID proporcionado
    if reporte:
        # Devuelve un diccionario con los datos del reporte
        return {
            'nombre': reporte[1],
            'departamento': reporte[2],
            'fecha': reporte[3],
            'descripcion': reporte[4]
        }
    else:
        # Si no se encuentra el reporte, devuelve None
        return None


@app.route('/ver_usuario')
def ver_usuario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('ver_usuario.html', usuarios=usuarios)


@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
        mysql.connection.commit()
        cur.close()

        flash('Usuario creado correctamente')
        return redirect(url_for('usuarios'))
    else:
        return render_template('error.html', message='Método no permitido')

@app.route('/usuarios', methods=['GET'])
def mostrar_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('usuarios.html', usuarios=usuarios)


if __name__ == '__main__':
    app.run(port=5000, debug=True)