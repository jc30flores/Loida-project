from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
session_flask = session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import numpy
from io import BytesIO
import base64
from base64 import b64encode
import time
import pandas as pd
from form import LoginForm, ClientesForm

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:diez203040@localhost:5432/database1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

db = SQLAlchemy(app)

#---------------------------CREACION DE LAS TABLAS DE LA BASE DE DATOS-------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
class Clientes(db.Model):
    """
    id: id automatico
    codigo: codigo de cliente, es un codigo que se le agregara aparte del id
    nombre: Ambos Nombres del cliente.
    apellidos: Ambos Apellidos del cliente
    num_dui: en formato string ya que llevara guion (obligatorio)
    foto_dui: id o codigo de donde se encontrara la imagen del DUI (opcional).
    num_nit: en formato string ya que llevara guiones (opcional)
    foto_nit: id o codigo de donde se encontrara la imagen del NIT (opcional)
    departamento: Nombre del departamento al que el cliente pertenece
    municipio: nombre del municipio al que pertenece el cliente
    ubicacion: Ubicacion de la localidad en la que reside en cliente
    genero: Masculino o Femenino, Hombre o Mujer, genero o sexo del cliente
    edad: edad del cliente
    celular: numero de celular del cliente
    aux_celular: numero auxiliar del cliente (obligatorio)
    hijos: cantidad de hijos que tiene el cliente (opcional)
    estado: estado civil del cliente. (casado, soltero, divorciado, comprometido, viudo, etc.)
    ocupacion: nombre del trabajo del cliente, o la ocupacion que ejerce
    empleo_dir: direccion del empleo del cliente (opcional)
    vivienda: situacion de la vivienda, alquilada o propia
    sueldo: sueldo o ingreso mensual del cliente (opcional)
    otros_ingresos: especificacion si tiene otros ingresos
    abono: el abono total que tiene el cliente, ya sea por uno o varios productos
    deuda: la deuda total con la que el cliente cuenta, ya sea por uno o varios productos
    f_ingreso: fecha que se ingreso al sistema
    confianza: opcion de si o no, si el cliente es un cliente de confianza.
    """    

    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)   
    codigo = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    num_dui = db.Column(db.String(10), unique=True)
    foto_dui = db.Column(db.LargeBinary)
    num_nit = db.Column(db.String(17), unique=True)
    foto_nit = db.Column(db.LargeBinary)
    departamento = db.Column(db.String(50))
    municipio = db.Column(db.String(50))
    ubicacion = db.Column(db.String(50))
    genero = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    celular = db.Column(db.String(9), unique=True)
    aux_celular = db.Column(db.String(9), unique=True)
    hijos = db.Column(db.Integer)
    estado = db.Column(db.String(20))
    ocupacion = db.Column(db.String(50))
    empleo_dir = db.Column(db.String())
    vivienda = db.Column(db.String(20))
    sueldo = db.Column(db.Integer)
    otros_ingresos = db.Column(db.String(50))
    abono = db.Column(db.Integer)
    deuda = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
    confianza = db.Column(db.String(3))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'num_dui': self.num_dui,
            'foto_dui': self.foto_dui,
            'num_nit': self.num_nit,
            'foto_nit': self.foto_nit,
            'departamento': self.departamento,
            'municipio': self.municipio,
            'ubicacion': self.ubicacion,
            'genero': self.genero,
            'edad': self.edad,
            'celular': self.celular,
            'aux_celular': self.aux_celular,
            'hijos': self.hijos,
            'estado': self.estado,
            'ocupacion': self.ocupacion,
            'empleo_dir': self.empleo_dir,
            'vivienda': self.vivienda,
            'sueldo': self.sueldo,
            'otros_ingresos': self.otros_ingresos,
            'abono': self.abono,
            'deuda': self.deuda,
            'f_ingreso': self.f_ingreso,
            'confianza': self.confianza
        }
    

class Familiares(db.Model):
    """
    id: id automatico
    codigo: codigo de familiar, es un codigo que se le agregara aparte del id
    nombre: Ambos Nombres del familiar.
    apellidos: Ambos Apellidos del familiar
    num_dui: en formato string ya que llevara guion (obligatorio)
    num_nit: en formato string ya que llevara guiones (opcional)
    departamento: Nombre del departamento al que el familiar pertenece
    municipio: nombre del municipio al que pertenece el familiar
    ubicacion: Ubicacion de la localidad en la que reside en familiar
    genero: Masculino o Femenino, Hombre o Mujer, genero o sexo del familiar
    edad: edad del familiar
    celular: numero de celular del familiar
    f_ingreso: fecha que se ingreso al sistema
    cliente_id: id del cliente al que pertenece el familiar
    """    
    
    __tablename__ = 'familiares'
    id = db.Column(db.Integer, primary_key=True)   
    codigo = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    num_dui = db.Column(db.String(10), unique=True)
    num_nit = db.Column(db.String(17), unique=True)
    departamento = db.Column(db.String(50))
    municipio = db.Column(db.String(50))
    ubicacion = db.Column(db.String(50))
    genero = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    celular = db.Column(db.String(9), unique=True)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Clientes', backref=db.backref('familiares', lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'num_dui': self.num_dui,
            'num_nit': self.num_nit,
            'departamento': self.departamento,
            'municipio': self.municipio,
            'ubicacion': self.ubicacion,
            'genero': self.genero,
            'edad': self.edad,
            'celular': self.celular,
            'f_ingreso': self.f_ingreso,
            'cliente_id': self.cliente_id
        }


class Vendedores(db.Model):
    """
    id: id automatico
    codigo: codigo de vendedor, es un codigo que se le agregara aparte del id
    nombre: Ambos Nombres del vendedor.
    apellidos: Ambos Apellidos del vendedor
    num_dui: en formato string ya que llevara guion (obligatorio)
    num_nit: en formato string ya que llevara guiones (opcional)
    sueldo_diario: sueldo diario del vendedor
    sueldo_total: sueldo del vendedor que se le ha pagado hasta la fecha
    cargo: cargo del vendedor
    dias_trabajo: dias de trabajo del vendedor en el mes
    comision_contado: comision que se le dara al vendedor por cada venta al contado que haga esto sera el total que ha ganado
    comision_credito: comision que se le dara al vendedor por cada venta al credito que haga esto sera el total que ha ganado
    total_sueldo_semanal: total de sueldo semanal del vendedor
    f_ingreso: fecha que se ingreso al sistema
    """
    __tablename__ = 'vendedores'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    num_dui = db.Column(db.String(10), unique=True)
    num_nit = db.Column(db.String(17), unique=True)
    sueldo_diario = db.Column(db.Integer)
    sueldo_total = db.Column(db.Integer)
    cargo = db.Column(db.String(50))
    dias_trabajo = db.Column(db.Integer)
    comision_contado = db.Column(db.Integer)
    comision_credito = db.Column(db.Integer)
    total_sueldo_semanal = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'num_dui': self.num_dui,
            'num_nit': self.num_nit,
            'sueldo_diario': self.sueldo_diario,
            'sueldo_total': self.sueldo_total,
            'cargo': self.cargo,
            'dias_trabajo': self.dias_trabajo,
            'comision_contado': self.comision_contado,
            'comision_credito': self.comision_credito,
            'total_sueldo_semanal': self.total_sueldo_semanal,
            'f_ingreso': self.f_ingreso
        }


class Credito(db.Model):
    """
    id: id automatico
    cliente_id: id del cliente que tiene el credito
    producto_id: id del producto que tiene el credito
    vendedor_id: id del vendedor que vendio el producto
    precio_uni: precio del producto por unidad
    cantidad: cantidad de productos en credito
    abono: lista de los abonos que se le ha hecho al credito tiene que ir conectado con la columna de fecha_de_abonos
    abono_total: abono total que se le ha hecho al credito
    fecha_de_abonos: lista de todas las fechas en las que ha abonado tiene que ir conectado con la columna abono
    deuda: deuda que tiene el cliente solo sera el total de la deuda que tiene el cliente
    fecha_proximo_cobro: fecha en la que se le debe de hacer el proximo cobro
    f_ingreso: fecha que se ingreso al sistema
    """
    __tablename__ = 'credito'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    precio_uni = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    abono = db.Column(db.String())
    abono_total = db.Column(db.Integer)
    fecha_de_abonos = db.Column(db.String())
    deuda = db.Column(db.Integer)
    fecha_proximo_cobro = db.Column(db.DateTime)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())

    #Aqui se crea la relacion de uno a muchos con la clase Clientes
    cliente = db.relationship('Clientes', backref=db.backref('credito', lazy='dynamic'))
    #Aqui se crea la relacion de uno a muchos con la clase Productos
    producto = db.relationship('Productos', backref=db.backref('credito', lazy='dynamic'))
    #Aqui se crea la relacion de uno a muchos con la clase Vendedores
    vendedor = db.relationship('Vendedores', backref=db.backref('credito', lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'producto_id': self.producto_id,
            'precio_uni': self.precio_uni,
            'cantidad': self.cantidad,
            'abono': self.abono,
            'abono_total': self.abono_total,
            'fecha_de_abonos': self.fecha_de_abonos,
            'deuda': self.deuda,
            'fecha_proximo_cobro': self.fecha_proximo_cobro,
            'f_ingreso': self.f_ingreso
        }
    

class Contado(db.Model):
    """
    id: id automatico
    cliente_id: id del cliente que tiene el credito
    producto_id: id del producto que tiene el credito
    vendedor_id: id del vendedor que vendio el producto
    precio_uni: precio del producto por unidad
    cantidad: cantidad de productos al contado
    saldo_total_cancelado: saldo total que se ha cancelado
    f_ingreso: fecha que se ingreso al sistema
    """
    __tablename__ = 'contado'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    precio_uni = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)
    saldo_total_cancelado = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())

    #Aqui se crea la relacion de uno a muchos con la clase Clientes
    cliente = db.relationship('Clientes', backref=db.backref('contado', lazy='dynamic'))
    #Aqui se crea la relacion de uno a muchos con la clase Productos
    producto = db.relationship('Productos', backref=db.backref('contado', lazy='dynamic'))
    #Aqui se crea la relacion de uno a muchos con la clase Vendedores
    vendedor = db.relationship('Vendedores', backref=db.backref('contado', lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'producto_id': self.producto_id,
            'precio_uni': self.precio_uni,
            'cantidad': self.cantidad,
            'saldo_total_cancelado': self.saldo_total_cancelado,
            'f_ingreso': self.f_ingreso
        }


class Productos(db.Model):
    """
    id: id automatico
    codigo: codigo del producto, es un codigo que se le agregara aparte del id
    nombre: nombre del producto
    descripcion: descripcion del producto
    precio_uni: precio del producto por unidad
    f_ingreso: fecha que se ingreso al sistema
    color: color del producto
    modelo: modelo del producto
    serie: serie del producto
    material: material del producto
    categoria: categoria del producto
    costo_uni: costo del producto por unidad
    cantidad: cantidad de productos en existencia
    """
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String())
    precio_uni = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
    color = db.Column(db.String(20))
    modelo = db.Column(db.String(20))
    serie = db.Column(db.String(20))
    material = db.Column(db.String(20))
    categoria = db.Column(db.String(20))
    costo_uni = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_uni': self.precio_uni,
            'f_ingreso': self.f_ingreso,
            'color': self.color,
            'modelo': self.modelo,
            'serie': self.serie,
            'material': self.material,
            'categoria': self.categoria,
            'costo_uni': self.costo_uni,
            'cantidad': self.cantidad
        }

#aqui va la tabla para los gastos y falta la tabla para los ingresos y los productos vendidos al contado.
#Crea una tabla para los gastos
class Gastos(db.Model):
    """
    id: id automatico
    nombre: nombre del gasto
    descripcion: descripcion del gasto
    monto: monto del gasto
    f_ingreso: fecha que se ingreso al sistema
    categoria: categoria del gasto (ejemplo: pagos de recibos y alquiler, sueldos, alimentacion, combustible, otros gastos.)
    numero_de_factura: numero de la factura del gasto (opcional)
    numero_de_referencia: numero de referencia del gasto (opcional)
    tipo_de_pago: tipo de pago del gasto (efectivo, tarjeta de credito, tarjeta de debito, cheque, transferencia, otros)
    """
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String())
    monto = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
    categoria = db.Column(db.String(20))
    numero_de_factura = db.Column(db.String(20))
    numero_de_referencia = db.Column(db.String(20))
    tipo_de_pago = db.Column(db.String(20))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'monto': self.monto,
            'f_ingreso': self.f_ingreso,
            'categoria': self.categoria,
            'numero_de_factura': self.numero_de_factura,
            'numero_de_referencia': self.numero_de_referencia,
            'tipo_de_pago': self.tipo_de_pago
        }


class Ingresos(db.Model):
    """
    id: id automatico
    nombre: nombre del ingreso
    descripcion: descripcion del ingreso
    monto: monto del ingreso
    f_ingreso: fecha que se ingreso al sistema
    proviene_de: de que tabla proviene este ingreso (ejemplo: Credito, Contado, Recibos_Virtuales, Facturas, etc.) esto sera para llevar un control de la tabla en la que buscaremos con el id que se proporcione en la siguiente columna.
    id_de_ingreso: id del ingreso que se obtendra de la tabla que se proporcione en la columna anterior.
    """
    __tablename__ = 'ingresos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String())
    monto = db.Column(db.Integer)
    f_ingreso = db.Column(db.DateTime, default=db.func.current_timestamp())
    proviene_de = db.Column(db.String(20))
    id_de_ingreso = db.Column(db.Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'monto': self.monto,
            'f_ingreso': self.f_ingreso,
            'proviene_de': self.proviene_de,
            'id_de_ingreso': self.id_de_ingreso
        }
    

class Recibos_Virtuales(db.Model):
    """
    codigo: codigo del recibo, es un codigo que se le agregara aparte del id
    id: id automatico
    fecha: fecha del recibo
    vendedor: nombre del vendedor que realizo el recibo esta va conectada con la tabla vendedores
    cliente: nombre del cliente que realizo el recibo esta conectada con la tabla clientes
    monto: monto que esta abonando el cliente
    producto: nombre del producto que esta abonando el cliente esto va conectado con la tabla Creditos para saber que producto esta abonando
    saldo_anterior: saldo anterior que tenia el cliente de igual manera estaran conectadas a la tabla Creditos
    saldo_actual: saldo actual que tiene el cliente de igual manera estaran conectadas a la tabla Creditos
    accion: esto es para saber si el cliente esta haciendo un abono, una prima, o la cancelacion del producto que obtuvo en credito o contado
    """
    __tablename__ = 'recibos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Clientes', backref=db.backref('recibos', lazy='dynamic'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    vendedor = db.relationship('Vendedores', backref=db.backref('recibos', lazy='dynamic'))
    monto = db.Column(db.Integer)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    producto = db.relationship('Productos', backref=db.backref('recibos', lazy='dynamic'))
    saldo_anterior = db.Column(db.Integer)
    saldo_actual = db.Column(db.Integer)
    accion = db.Column(db.String(20))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'fecha': self.fecha,
            'cliente_id': self.cliente_id,
            'vendedor_id': self.vendedor_id,
            'monto': self.monto,
            'producto_id': self.producto_id,
            'saldo_anterior': self.saldo_anterior,
            'saldo_actual': self.saldo_actual,
            'accion': self.accion
        }


class Facturas(db.Model):
    """
    codigo: codigo de la factura, es un codigo que se le agregara aparte del id
    id: id automatico
    fecha: fecha de la factura
    vendedor: nombre del vendedor que realizo la factura
    cliente: nombre del cliente que realizo la factura
    """
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Clientes', backref=db.backref('facturas', lazy='dynamic'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'))
    vendedor = db.relationship('Vendedores', backref=db.backref('facturas', lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'fecha': self.fecha,
            'cliente_id': self.cliente_id,
            'vendedor_id': self.vendedor_id
        }
    
with app.app_context():
    db.create_all()

session = db.session

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['usuario'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            flash(error)
            return redirect(url_for('login'))
        else:
            flash('You were logged in')
            return redirect(url_for('menu_principal'))
    else:
        return render_template('login.html', form=LoginForm())
    
@app.route('/login/menu_principal', methods=['GET', 'POST'])
def menu_principal():
    return render_template('menu_principal.html')

@app.route('/login/menu_principal/registro_de_clientes', methods=['GET', 'POST'])
def registro_de_clientes():
    if request.method == 'POST':
        cliente = Clientes(nombre=request.form['nombre'], direccion=request.form['direccion'], telefono=request.form['telefono'], email=request.form['email'])
        session.add(cliente)
        session.commit()
        flash('Cliente registrado')
        return redirect(url_for('registro_de_clientes'))
    else:
        return render_template('registro_de_clientes.html', form=ClientesForm())
    


if __name__ == '__main__':
    app.secret_key = 'secret_key10'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)       