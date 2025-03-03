class CustomerRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'mysql_customer'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'customer':
            return 'mysql_customer'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'mysql_customer' or obj2._state.db == 'mysql_customer':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'customer':
            return db == 'mysql_customer'
        return None

class BookRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'book':
            return 'mongo_book'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'book':
            return 'mongo_book'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'mongo_book' or obj2._state.db == 'mongo_book':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'book':
            return db == 'mongo_book'
        return None

class CartRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'cart':
            return 'postgres_cart'  
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'cart':
            return 'postgres_cart'  
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'postgres_cart' or obj2._state.db == 'postgres_cart':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'cart':
            return db == 'postgres_cart'  
        return None

class OrderRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['order', 'paying', 'shipping']:
            return 'postgres_order'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['order', 'paying', 'shipping']:
            return 'postgres_order'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'postgres_order' or obj2._state.db == 'postgres_order':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ['order', 'paying', 'shipping']:
            return db == 'postgres_order'
        return None

class MobileRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'mobile':
            return 'mongo_mobile'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'mobile':
            return 'mongo_mobile'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'mongo_mobile' or obj2._state.db == 'mongo_mobile':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'mobile':
            return db == 'mongo_mobile'
        return None

class ShoesRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'shoes':
            return 'mongo_shoes'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'shoes':
            return 'mongo_shoes'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'mongo_shoes' or obj2._state.db == 'mongo_shoes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'shoes':
            return db == 'mongo_shoes'
        return None

class ClothesRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'clothes':
            return 'mongo_clothes'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'clothes':
            return 'mongo_clothes'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._state.db == 'mongo_clothes' or obj2._state.db == 'mongo_clothes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'clothes':
            return db == 'mongo_clothes'
        return None
