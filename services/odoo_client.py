import requests
import random


class OdooClient:
    def __init__(self, base_url: str, db: str):
        self.base_url = base_url.rstrip('/') + '/'
        self.db = db
        self.session = requests.Session()

    def authenticate(self, login: str, password: str):
        url = self.base_url + 'web/session/authenticate'
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {"db": self.db, "login": login, "password": password},
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        uid = data["result"]["uid"]
        return True, uid, None

    def get_partners(self, limit=50):
        url = self.base_url + 'web/dataset/call_kw'
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "res.partner",
                "method": "search_read",
                "args": [[]],
                "kwargs": {
                    "fields": ["id", "name", "email"],
                    "limit": limit
                }
            },
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        return True, data.get("result", []), None


    def get_products(self, limit=50):
        url = self.base_url + "web/dataset/call_kw"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "product.product",
                "method": "search_read",
                "args": [[]],
                "kwargs": {
                    "fields": ["id", "name", "list_price"],
                    "limit": limit
                }
            },
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        return True, data["result"], None

    def create_order(self, partner_id: int):
        url = self.base_url + "web/dataset/call_kw"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "sale.order",
                "method": "create",
                "args": [{
                    "partner_id": partner_id
                }],
                "kwargs": {}
            },
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        return True, data["result"], None

    def add_order_line(self, order_id: int, product_id: int, quantity: int, price_unit: float):
        url = self.base_url + "web/dataset/call_kw"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "sale.order.line",
                "method": "create",
                "args": [{
                    "order_id": order_id,
                    "product_id": product_id,
                    "product_uom_qty": quantity,
                    "price_unit": price_unit,
                    "name": "Ligne ajoutée via API"
                }],
                "kwargs": {}
            },
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        return True, data["result"], None

    def get_order_status(self, order_id: int):
        url = self.base_url + "web/dataset/call_kw"
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "sale.order",
                "method": "read",
                "args": [[order_id]],
                "kwargs": {"fields": ["state"]}
            },
            "id": random.randint(1, 10**6)
        }

        resp = self.session.post(url, json=payload)
        data = resp.json()

        if "error" in data:
            return False, None, data["error"]["data"]["message"]

        return True, data["result"][0]["state"], None