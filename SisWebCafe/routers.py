class CassandraRouter:
    """
    Router para dirigir las operaciones de modelos específicos a Cassandra
    y el resto a PostgreSQL
    """
    
    def db_for_read(self, model, **hints):
        """
        Determina qué base de datos usar para lecturas
        """
        if model._meta.app_label == 'menu':
            # Los modelos de productos van a Cassandra
            if model.__name__ in ['Categoria', 'Subcategoria', 'Producto', 'AtributoSubcategoria']:
                return 'cassandra'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Determina qué base de datos usar para escrituras
        """
        if model._meta.app_label == 'menu':
            # Los modelos de productos van a Cassandra
            if model.__name__ in ['Categoria', 'Subcategoria', 'Producto', 'AtributoSubcategoria']:
                return 'cassandra'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Determina si se permite una relación entre objetos
        """
        # No permitimos relaciones entre modelos de diferentes bases de datos
        if obj1._state.db == obj2._state.db:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        No permitir migraciones para modelos de Cassandra
        """
        if app_label == 'menu':
            return False
        return True