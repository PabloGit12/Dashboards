from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask import send_file
# from reportlab.pdfgen import canvas
from io import BytesIO
# from reportlab.lib.pagesizes import letter



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
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

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        usuario = request.form['txtdepartamento']
        contraseña = request.form['txtcontraseña']

        cur = mysql.connection.cursor()
        cur.execute("SELECT contraseña FROM user WHERE departamento = %s", (usuario,))
        usuario_encontrado = cur.fetchone()
        cur.close()

        if usuario_encontrado:
            contraseña_encontrada = usuario_encontrado[0]  # Obtener la contraseña almacenada en la base de datos

            # Verificar si la contraseña ingresada coincide con la contraseña almacenada
            if bcrypt.check_password_hash(contraseña_encontrada, contraseña):
                # Contraseña correcta, redirigir al usuario
                if usuario == "jefe":
                    return redirect(url_for('jefe'))
                elif usuario == "auxiliar":
                    return redirect(url_for('auxiliar'))
                else:
                    return redirect(url_for('cliente'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
                return redirect(url_for('index'))
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

@app.route('/editarDepartamento/<int:id>', methods=['GET', 'POST'])
def editarDepartamento(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        nombre = request.form['nombre']
        responsable = request.form['responsable']
        
        # Actualizar el departamento en la base de datos
        cur.execute("UPDATE departamentos SET nombre = %s, responsable = %s WHERE id = %s", (nombre, responsable, id))
        mysql.connection.commit()
        
        flash('Departamento actualizado correctamente', 'success')
        cur.close()
        return redirect('/seeDepartamentos')

    # Obtener los datos del departamento a editar
    cur.execute("SELECT * FROM departamentos WHERE id = %s", (id,))
    departamento = cur.fetchone()
    cur.close()
    return render_template('editarDepartamento.html', departamento=departamento)

@app.route('/editarUsuario/<int:id>', methods=['GET', 'POST'])
def editarUsuario(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        nombre = request.form['nombre']
        email = request.form['email']
        
        # Actualizar el departamento en la base de datos
        cur.execute("UPDATE Usuarios SET nombre = %s, email = %s WHERE id = %s", (nombre, email, id))
        mysql.connection.commit()
        
        flash('Usuario actualizado correctamente', 'success')
        cur.close()
        return redirect('/ver_usuario')

    # Obtener los datos del departamento a editar
    cur.execute("SELECT * FROM Usuarios WHERE id = %s", (id,))
    usuarios = cur.fetchone()
    cur.close()
    return render_template('editarUsuario.html', usuarios=usuarios)



    
@app.route('/seeDepartamentos', methods=['GET'])
def seeDepartamentos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM departamentos")
    departamentos = cur.fetchall()
    cur.close()
    print(departamentos)  # Añade esta línea para imprimir los resultados
    return render_template('seeDepartamentos.html', departamentos=departamentos)

@app.route('/eliminarDepartamento/<int:id>', methods=['GET', 'POST'])
def eliminarDepartamento(id):
    # Conexión a la base de datos y cursor
    cur = mysql.connection.cursor()
    
    try:
        # Ejecutar la consulta SQL para eliminar el departamento con el ID dado
        cur.execute("DELETE FROM departamentos WHERE id = %s", (id,))
        # Confirmar la eliminación
        mysql.connection.commit()
    except Exception as e:
        # Si ocurre algún error, deshacer la operación y manejar el error
        mysql.connection.rollback()
        print("Error al eliminar el departamento:", e)
    finally:
        # Cerrar el cursor
        cur.close()
    
    # Redirigir a la página 'seeDepartamentos' después de eliminar el departamento
    return redirect(url_for('seeDepartamentos'))
@app.route('/eliminarUsuario/<int:id>', methods=['GET', 'POST'])
def eliminarUsuario(id):
    # Conexión a la base de datos y cursor
    cur = mysql.connection.cursor()
    
    try:
        # Ejecutar la consulta SQL para eliminar el departamento con el ID dado
        cur.execute("DELETE FROM Usuarios WHERE id = %s", (id,))
        # Confirmar la eliminación
        mysql.connection.commit()
    except Exception as e:
        # Si ocurre algún error, deshacer la operación y manejar el error
        mysql.connection.rollback()
        print("Error al eliminar el Usuarios:", e)
    finally:
        # Cerrar el cursor
        cur.close()
    
    # Redirigir a la página 'seeDepartamentos' después de eliminar el departamento
    return redirect(url_for('ver_usuario'))



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


@app.route('/ver_usuario', methods=['GET'])
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

@app.route('/perfil_auxiliar')
def perfil_auxiliar():
    # Consultar la base de datos para obtener la información del usuario con ID 4
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = 4")
    usuario = cur.fetchone()  # Obtener el primer usuario encontrado (debería ser el único con ID 4)
    cur.close()

    # Renderizar la plantilla HTML y pasar los datos del usuario
    return render_template('PerfilAuxiliar.html', usuario=usuario)

@app.route('/editarPerfil/<int:id>', methods=['GET', 'POST'])
def editarPerfil(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        nombre = request.form['nombre']
        email = request.form['email']
        
        # Actualizar el departamento en la base de datos
        cur.execute("UPDATE Usuarios SET nombre = %s, email = %s WHERE id = %s", (nombre, email, id))
        mysql.connection.commit()
        
        flash('Perfil actualizado correctamente', 'success')
    
    # Obtener los datos del departamento a editar
    cur.execute("SELECT * FROM Usuarios WHERE id = %s", (id,))
    usuarios = cur.fetchone()
    cur.close()
    
    return render_template('editarPerfil.html', usuarios=usuarios)

@app.route('/control_tickets', methods=['GET', 'POST'])
def control_tickets():
    if request.method == 'POST':
        # Lógica para filtrar y ordenar las solicitudes por fecha
        ordenamiento = request.form['ordenamiento']
        # Actualiza tu consulta SQL según el ordenamiento seleccionado

    # Lógica para obtener las solicitudes
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, departamento, tipo_soporte, detalles, fecha FROM solicitudes WHERE departamento = 'auxiliar'")
    solicitudes = cur.fetchall()
    cur.close()

    return render_template('ControlTickets.html', solicitudes=solicitudes)

@app.route('/comentarios_mensajes')
def comentarios_mensajes():
    cur = mysql.connection.cursor()

    # Obtener los mensajes recibidos del jefe
    cur.execute("SELECT id, mensaje, responsable FROM mensajes WHERE dirigido = 'auxiliar'")
    mensajes_recibidos = cur.fetchall()

    # Obtener los mensajes enviados por el auxiliar
    cur.execute("SELECT id, mensaje, responsable, dirigido FROM mensajes WHERE responsable = 'auxiliar'")
    mensajes_enviados = cur.fetchall()

    cur.close()

    return render_template('ComentariosMensajes.html', mensajes_recibidos=mensajes_recibidos, mensajes_enviados=mensajes_enviados)
from flask import request

@app.route('/mensaje', methods=['GET', 'POST'])
def mensaje():
    if request.method == 'POST':
        mensaje_texto = request.form['mensaje']
        dirigido_a = request.form['dirigido']
        de = request.form['de']

        # Aquí puedes guardar el mensaje en la base de datos
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO mensajes (mensaje, responsable, dirigido) VALUES (%s, %s, %s)", (mensaje_texto, de, dirigido_a))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auxiliar'))  # Redirige a la página principal después de guardar el mensaje
        except Exception as e:
            print("Error al guardar el mensaje:", e)
            # Maneja el error apropiadamente, por ejemplo, mostrar un mensaje de error al usuario

    return render_template('Mensaje.html')

@app.route('/mensajesjefe')
def mensajesjefe():
    cur = mysql.connection.cursor()

    # Obtener los mensajes recibidos del jefe
    cur.execute("SELECT id, mensaje, responsable FROM mensajes WHERE dirigido = 'Jefe'")
    mensajes_recibidos = cur.fetchall()

    # Obtener los mensajes enviados por el auxiliar
    cur.execute("SELECT id, mensaje, responsable, dirigido FROM mensajes WHERE responsable = 'Jefe'")
    mensajes_enviados = cur.fetchall()

    cur.close()

    return render_template('MensajesJefe.html', mensajes_recibidos=mensajes_recibidos, mensajes_enviados=mensajes_enviados)

@app.route('/mensajejefesend', methods=['GET', 'POST'])
def mensajejefesend():
    if request.method == 'POST':
        mensaje_texto = request.form['mensaje']
        dirigido_a = request.form['dirigido']
        de = request.form['de']

        # Aquí puedes guardar el mensaje en la base de datos
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO mensajes (mensaje, responsable, dirigido) VALUES (%s, %s, %s)", (mensaje_texto, de, dirigido_a))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auxiliar'))  # Redirige a la página principal después de guardar el mensaje
        except Exception as e:
            print("Error al guardar el mensaje:", e)
            # Maneja el error apropiadamente, por ejemplo, mostrar un mensaje de error al usuario

    return render_template('EnviarMensaje.html')
if __name__ == '__main__':
    app.run(port=5000, debug=True)