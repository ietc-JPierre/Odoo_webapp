class Product:
    def __init__(self, raw: dict):
        self.id = raw.get('id')
        self.name = raw.get('name')
        self.default_code = raw.get('default_code')
        self.list_price = raw.get('list_price')
        self.qty_available = raw.get('qty_available')
        self.categ_id = raw.get('categ_id')
        self.max_guests = raw.get('max_guests')