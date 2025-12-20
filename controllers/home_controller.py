from flask import Blueprint, render_template, request, flash
from services.odoo_client import OdooClient

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', products=None)

@home_bp.route('/connect', methods=['POST'])
def connect():
    url = request.form.get('url', '')
    db = request.form.get('databaseName', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    client = OdooClient(url, db)

    # ✅ authenticate() retourne (ok, uid, err)
    ok, uid, err = client.authenticate(username, password)
    if not ok:
        flash(f"Connection failed: {err}", 'alert-danger')
        return render_template('index.html', products=None)

    # ✅ uid est un entier, pas un dict
    ok, result, err = client.get_products()
    if not ok:
        flash(f"Connected but failed to fetch products: {err}", 'alert-danger')
        return render_template('index.html', products=None)

    products = result or []

    flash(f"Connection successful! UID: {uid}. Found {len(products)} products.", 'alert-success')

    return render_template('index.html', products=products, user_id=uid)