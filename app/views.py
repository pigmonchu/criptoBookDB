from flask import render_template, request, redirect, url_for
from app import app
import csv
import os

ficherotransacciones = "data/transacciones.dat"
nuevoficherotransacciones = 'data/newtransacciones.dat'
fields = ['fecha', 'hora', 'descripcion', 'monedaComprada', 'cantidadComprada', 'monedaPagada', 'cantidadPagada']

def makeDict(lista):
    diccionario = {}
    for ix, field in enumerate(fields):
        diccionario[field] = lista[ix]
    return diccionario

def makeReg(form):
    return '{},{},"{}",{},{},{},{}\n'.format(form['fecha'],form['hora'],form['descripcion'],form['monedaComprada'],form['cantidadComprada'],form['monedaPagada'],form['cantidadPagada'])

@app.route('/')
def index():
    transacciones = open(ficherotransacciones, 'r')
    csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )

    movimientos = []
    for campos in csvreader:
        camposdict = makeDict(campos)
        '''
        camposdict = {
            'fecha': campos[0],
            'hora': campos[1],
            'descripcion': campos[2],
            'monedaComprada': campos[3],
            'cantidadComprada': campos[4],
            'monedaPagada': campos[5],
            'cantidadPagada': campos[6],
        }
        '''
        movimientos.append(camposdict)

    return render_template('index.html', movimientos=movimientos)

@app.route('/nuevacompra', methods=['GET', 'POST'])
def nuevacompra():
    if request.method == 'GET':
        if len(request.values) == 0 or request.values.get('btnselected') == 'Nueva':
            return render_template('nuevacompra.html')
        else:
            if request.values.get('ix') != None:
                registroseleccionado = int(request.values.get('ix'))
                transacciones = open(ficherotransacciones, 'r')
                csvreader = csv.reader(transacciones, delimiter=',', quotechar='"' )
                for numreg, registro in enumerate(csvreader):
                    if numreg == registroseleccionado:
                        camposdict = makeDict(registro)
                        camposdict['registroseleccionado'] = registroseleccionado
                        return render_template('modificacompra.html', registro=camposdict)
                return 'Movimiento no encontrado'
            else:
                return redirect(url_for('index'))
    else:
        datos = request.form
        transacciones = open(ficherotransacciones, "a+")
        registro = makeReg(request.form)
        
        transacciones.write(registro)
        transacciones.close()
        return redirect(url_for('index'))

@app.route('/modificacompra', methods=['POST'])
def modificacompra():
    '''
        1. - Recuperar los datos del formulario de request - check
        2. - Recuperar el registro al que corresponden - check
            2.1. Abrir fichero en formato lectura -check
            2.2 Crear fichero nuevo en formato escritura - check
            2.3 Copiar todos los registros hasta el encontrado en nuevo fichero - check
        3. - Modificar ese registro
            3.1 - Sustituir el registro a modificar por los datos del formulario
            3.4 - Grabar en fichero nuevo
            3.5 - Grabar en fichero nuevo el resto de registros - check
            3.6 - Borrar fichero antiguo
            3.7 - renombrar fichero nuevo

        4. - Devolver una página que diga que todo OK
    '''
    transacciones = open(ficherotransacciones, 'r')
    newtransacciones = open(nuevoficherotransacciones, 'w+')
    
    registroseleccionado = int(request.form['registroseleccionado'])

    linea = transacciones.readline()
    numreg = 0
    while linea != "":
        if numreg == registroseleccionado:
            linea = makeReg(request.form)

        newtransacciones.write(linea)
        linea = transacciones.readline()
        numreg += 1

    transacciones.close()
    newtransacciones.close()
    os.remove(ficherotransacciones)
    os.rename(nuevoficherotransacciones, ficherotransacciones)

    return redirect(url_for('index'))

    
