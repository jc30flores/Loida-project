from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, DateField, TextAreaField, SelectMultipleField, DecimalField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_wtf.file import FileAllowed, FileField


class LoginForm(Form):
    usuario = StringField('Usuario:', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña:', validators=[InputRequired(), Length(min=4, max=25)])
    
class ClientesForm(Form):
    nombres = StringField('Nombres:', validators=[InputRequired(), Length(min=2, max=50)])
    apellidos = StringField('Apellidos:', validators=[InputRequired(), Length(min=2, max=50)])
    dui = IntegerField('Número de DUI:', validators=[InputRequired()])
    foto_dui = FileField('Foto de DUI:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten archivos con extensión .jpg, .jpeg o .png')], label='Foto de DUI')
    nit = IntegerField('Número de NIT:')
    foto_nit = FileField('Foto de NIT:', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten archivos con extensión .jpg, .jpeg o .png')])
    departamento = SelectField('Departamento:', choices=[('San Salvador'), ('La Libertad'), ('La Paz'), ('Santa Ana'), ('Sonsonate'), ('Ahuachapán'), ('Chalatenango'), ('Cuscatlán'), ('Usulután'), ('Morazán'), ('Cabañas'), ('La Unión')], validators=[InputRequired()])
    municipio = StringField('Municipio:', validators=[InputRequired(), Length(min=2, max=50)])
    ubicacion_localidad = TextAreaField('Ubicación de su localidad:', validators=[InputRequired(), Length(min=5, max=200)])
    genero = SelectField('Género:', choices=[('M', 'Hombre'), ('F', 'Mujer')], validators=[InputRequired()])
    edad = IntegerField('Edad:', validators=[InputRequired()])
    celular = IntegerField('Número de celular:', validators=[InputRequired()])
    celular_auxiliar = IntegerField('Número de celular auxiliar:', validators=[InputRequired()])
    cantidad_hijos = IntegerField('Cantidad de hijos:')
    estado_civil = SelectField('Estado civil:', choices=[('Soltero/a', 'Soltero/a'), ('Casado/a', 'Casado/a'), ('Divorciado/a', 'Divorciado/a'), ('Viudo/a', 'Viudo/a')], validators=[InputRequired()])
    ocupacion = StringField('Nombre de la ocupación o trabajo del cliente:', validators=[InputRequired(), Length(min=5, max=100)])
    direccion_empleo = StringField('Dirección de su empleo:')
    vivienda = SelectField('Tipo de vivienda:', choices=[('alquilada', 'Alquilada'), ('propia', 'Propia')], validators=[InputRequired()])
    ingreso_mensual = DecimalField('Sueldo o ingreso mensual:')
    otros_ingresos = TextAreaField('Otros ingresos:')
