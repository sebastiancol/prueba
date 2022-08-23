
from flask import Flask, render_template, request ,redirect,url_for, flash
import os
import psycopg2

app= Flask(__name__)

#base de datos
PSQL_HOST ="ec2-3-224-184-9.compute-1.amazonaws.com"
PSQL_PORT = "5432"
PSQL_USER = "aynmyqyugyiced"
PSQL_PASS = "1ced5c583c86768d23c576eadacacbd6a3bfe12650f0d0c0525bae2d677671b8"
PSQL_DB = "d91tdfva64adl6"
connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
conn = psycopg2.connect(connstr)
cursor = conn.cursor()
app.secret_key='mysecretkey'

#landing page
@app.route('/')
def init():
    return render_template('page.html')

#principal
@app.route('/index')
def index():
    usuarios = select_info()
    return render_template('introduce.html', data=get_mark() ,usuarios= usuarios)
 
#boton cancelar
@app.route('/cancel')    
def cancel():
    return redirect(url_for('index'))

#obtener marca
def get_mark():
    return {
        'ACER':'ACER',
        'H.P':'H.P',
        'LENOVO':'LENOVO',
        'DELL':'DELL',
        'MSI':'MSI',
    }

#agregar registro
@app.route('/add_info',methods=['POST'])
def add_info():
    try:
        if request.method =='POST':
            documento=request.form['documento']
            nombre=request.form['nombre']
            ape=request.form['ape']
            email=request.form['e-mail']
            contraseña=request.form['pass']
            marca=request.form['marca_portatil']    
            conn = psycopg2.connect(connstr)
            cursor= conn.cursor()        
            cursor.execute('INSERT INTO users (firstname,lastname,identification,email, password,computer) values (%s,%s,%s,%s,%s,%s,%s)',
            (nombre,ape,documento,email,contraseña,marca))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registro Agregado') 
            return redirect(url_for('index')) 
    except Exception as err:
        flash('La cedula ya existe')
        return redirect(url_for('index'))

#traer informacion        
def select_info():
    conn = psycopg2.connect(connstr)
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    cursor.close()     
    return data 
      
#actualizar registros
@app.route('/update_info/<string:id>', methods=['POST','GET'])
def update_info(id):
    conn = psycopg2.connect(connstr)
    cursor= conn.cursor()
    try:
        if request.method == 'GET':
            cursor.execute('select * from users where id ={}'.format(id)) 
            data = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()  
            datos = data[0]
            return render_template('update.html',usuarios=datos,data=get_mark() )
        else:
            documento=request.form['documento']
            nombre=request.form['nombre']
            ape=request.form['ape']
            fecha=request.form['fecha']
            marca=request.form['marca_portatil']    
            cursor.execute(""" 
                UPDATE users 
                SET firstname=%s,
                lastname=%s, 
                identification=%s, 
                email=%s,
                password=%s,
                fecha=%s
                WHERE id=%s """, (id, documento,nombre,ape,marca,fecha))
            conn.commit()
            cursor.close()
            conn.close()  
            flash('Registro Actualizado') 
            return redirect(url_for('index'))
    except Exception as err:
        flash('El registro de la cedula ya existe')
        return redirect(url_for('update_info'))      

#eliminar informacion
@app.route('/delete_info/<string:id>')
def delete_info(id):


    conn = psycopg2.connect(connstr)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user WHERE id={}'.format(id))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Registro Eliminado') 
    return redirect(url_for('index'))

#ejecucion de la aplicacion
if __name__ == '__main__':
    app.run(port=3000, debug=True)   