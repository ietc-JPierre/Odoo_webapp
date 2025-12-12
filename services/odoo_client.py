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
        resp = self.session.post(url, json=payload, timeout=10)
        if not resp.ok:
            return False, None, f"HTTP {resp.status_code}"
        data = resp.json()
        if 'error' in data:
            msg = data['error'].get('data', {}).get('message', 'Authentication failed')
            return False, None, msg
        uid = data.get('result', {}).get('uid')
        session_id = None
        for c in self.session.cookies:
            if c.name == 'session_id':
                session_id = c.value
        if uid and uid > 0:
            return True, {"uid": uid, "session_id": session_id or "Cookie not found"}, None
        return False, None, "Invalid credentials"

    def get_products(self, uid):
        url = self.base_url + 'web/dataset/call_kw'
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "product.product",
                "method": "search_read",
                "args": [[["create_uid", "=", uid]]],  
                "kwargs": {
                    "fields": ["id", "name", "default_code", "list_price", "qty_available", "categ_id", "max_guests"],
                    "limit": 50
                }
            },
            "id": random.randint(1, 10**6)
        }
        resp = self.session.post(url, json=payload, timeout=10)
        if not resp.ok:
            return False, None, f"HTTP {resp.status_code}"
        data = resp.json()
        if 'error' in data:
            msg = data['error'].get('data', {}).get('message', 'RPC error')
            return False, None, msg
        return True, data.get('result', []), None