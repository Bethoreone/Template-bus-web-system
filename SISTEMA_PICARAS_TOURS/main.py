from datetime import datetime
from msilib import datasizemask
from MySQLdb import connect
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'picaras_tours'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/picaras_tours/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_usuarios1 WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            print(account)
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            
            session['id'] = account['id_usuario']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/picaras_tours/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/picaras_tours/formulario_viajes')
def formulario_viajes():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes1")
        dataselect = cursor.fetchall()
       
        return render_template('formulario_viajes.html', data=dataselect)
    
    return redirect(url_for('home'))


@app.route('/picaras_tours/formulario_clientes')
def formulario_clientes():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_clientes1")
        dataselect = cursor.fetchall()
       
        return render_template('formulario_clientes.html', data=dataselect)
    
    return redirect(url_for('home'))


@app.route('/picaras_tours/reportes')
def reportes():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes1 WHERE MONTH(fecha_salida)< DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 6 MONTH);")
        dataselect2 = cursor.fetchall()
        
        return render_template('reportes.html', data=dataselect2)
   
    return redirect(url_for('home'))



@app.route('/picaras_tours/pasajeros')
def tablapasajeros():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_clientes1")
        dataselect2 = cursor.fetchall()
        
        return render_template('pasajeros.html', data=dataselect2)
   
    return redirect(url_for('home'))





@app.route('/viajesform', methods=['POST', 'GET'])
def formviaje():
    
 
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        nombre_viaje = request.form.get('nombreviaje')
        destino = request.form.get('destino')
        fecha_salida = request.form.get('fechasalida')
        fecha_regreso = request.form.get('fecharegreso')
        precio = request.form.get('precio')
        
        cursor.execute("INSERT INTO tb_viajes1(nombre_viaje, destino,  fecha_salida, fecha_regreso, precio) VALUES (%s, %s, %s, %s ,%s)",(nombre_viaje, destino,  fecha_salida, fecha_regreso, precio))
        mysql.connection.commit()
        
        
    
        return render_template('formulario_viajes.html')
    
@app.route('/clientesform', methods=['POST', 'GET'])
def formclientes():
    
 
    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        nombre_cliente = request.form.get('nombrecliente')
        edad = request.form.get('edad')
        id_viaje = request.form.get('idviaje')
        estado_pago = request.form.get('saldodeudor2')
        saldo_pago = request.form.get('saldopago')
        cursor.execute("INSERT INTO tb_clientes1(nombre_cliente, edad, estado_pago, saldo_pago, id_viaje) VALUES (%s, %s, %s, %s ,%s)",(nombre_cliente, edad, estado_pago, saldo_pago, id_viaje))
        mysql.connection.commit()
        
        
    
        return render_template('formulario_clientes.html')
        

@app.route('/plantilla')
def plantilla():
    print("plantilla")
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes1 WHERE MONTH(fecha_salida)< DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 6 MONTH);")
        viajes = cursor.fetchall()
    
    
        return render_template('plantilla.html', data = viajes)
    

@app.route('/nombreviaje', methods=['POST', 'GET'])
def nombreviaje():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes1 WHERE MONTH(fecha_salida)< DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 6 MONTH);")
        viajes = cursor.fetchall()
       
   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        valuenombreviaje = request.form.get('nombreviaje')
        
       
    if valuenombreviaje == '':
        
        viajeselect = ""
        idviajeselect = ""  
        valueviajeid = ""
        valuenombreviaje = ""
       
        return render_template('plantilla.html',data = viajes)
                              
    else:
        query_string = ("SELECT (id_viaje) FROM tb_viajes1 WHERE nombre_viaje = %s")
        cursor.execute(query_string,(valuenombreviaje,))
        data_viajeid = cursor.fetchone()
        valueviajeid = data_viajeid['id_viaje']
        
        return render_template('plantilla.html',  viajeselect = str(valuenombreviaje), data = viajes, idviajeselect = valueviajeid)
       

@app.route('/asiento', methods=['POST', 'GET'])
def noasiento():
    
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM tb_viajes1 WHERE MONTH(fecha_salida)< DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 6 MONTH);")
        viajes = cursor.fetchall()
        mysql.connection.commit()
        
        viajeselectdetails = request.form.get('nombreviajedetails')
        datonoasiento = request.values.get('asiento')
        viajeid = request.form["idviaje"]
        
        

        if viajeid == "":
            if viajeselectdetails != "":
                query_string = ("SELECT id_viaje FROM tb_viajes1 WHERE nombre_viaje = %s")
                cursor.execute(query_string,(viajeselectdetails,))
                idviajeencontrado = cursor.fetchone()
                viajeid = idviajeencontrado['id_viaje']
            else:
                print("No hay viaje seleccionado")

        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_string = ("SELECT * FROM tb_clientes1 WHERE id_viaje =  %s AND no_asiento = %s")
        # query_string = ("SELECT (id_cliente) FROM (tb_clientes1) INNER JOIN tb_viajes1 ON (tb_clientes1.id_viaje = tb_viajes1.id_viaje) WHERE no_asiento = %s")
        cursor.execute(query_string,(viajeid,datonoasiento,))
        identificador = cursor.fetchone()
        
        if identificador != None:
            idcliente = identificador.get('id_cliente')
            mysql.connection.commit()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query_string = ("SELECT (nombre_cliente) FROM (tb_clientes1) WHERE id_cliente = %s")
            cursor.execute(query_string,(idcliente,))
            datonombre = cursor.fetchone()
            nombrecliente = datonombre.get('nombre_cliente')
            mysql.connection.commit()
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query_string = ("SELECT (estado_pago) FROM (tb_clientes1) WHERE id_cliente = %s")
            cursor.execute(query_string,(idcliente,))
            datopago = cursor.fetchone()
            estadocliente = datopago.get('estado_pago')
            mysql.connection.commit()
        else:
            print("No se encontro")
            idcliente = ""
            nombrecliente = ""
            datonoasiento = ""
            estadocliente = ""
            data_asiento = ""
            data_nombre = ""
            data_pago = ""
            data = ""
            
        return render_template('plantilla.html', viajeselect = viajeselectdetails, data_asiento = datonoasiento, data_nombre = nombrecliente, data_pago = estadocliente, data = viajes)







        

