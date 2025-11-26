# menu/models.py
from django_cassandra_engine.models import DjangoCassandraModel
from cassandra.cqlengine import columns
import uuid

class Categoria(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    nombre = columns.Text(required=True)
    descripcion = columns.Text()
    activo = columns.Boolean(default=True)

    class Meta:
        get_pk_field = 'id'

class Subcategoria(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    categoria_id = columns.UUID(required=True, index=True)
    nombre = columns.Text(required=True)
    descripcion = columns.Text()
    activo = columns.Boolean(default=True)

    class Meta:
        get_pk_field = 'id'

class AtributoSubcategoria(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    subcategoria_id = columns.UUID(required=True, index=True)  
    nombre = columns.Text(required=True)
    tipo = columns.Text(required=True) 
    requerido = columns.Boolean(default=False)
    opciones = columns.List(value_type=columns.Text)

    class Meta:
        get_pk_field = 'id'

class Producto(DjangoCassandraModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    categoria_id = columns.UUID(required=True, index=True)
    subcategoria_id = columns.UUID(index=True)
    nombre = columns.Text(required=True)
    descripcion = columns.Text()
    precio = columns.Decimal(required=True)
    imagen = columns.Text()
    stock = columns.Integer(default=0)
    activo = columns.Boolean(default=True)
    atributos = columns.Map(key_type=columns.Text, value_type=columns.Text)
    fecha_creacion = columns.DateTime()
    ultima_actualizacion = columns.DateTime()
    puntos_extra = columns.Integer(default=0)
    
    class Meta:
        get_pk_field = 'id'