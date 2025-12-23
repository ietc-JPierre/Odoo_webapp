from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from services.odoo_client import OdooClient

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', products=None)


@home_bp.route('/connect', methods=['POST'])
def connect():
    url = request.form.get('url', '').rstrip('/') + '/'
    db = request.form.get('databaseName', '')
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    client = OdooClient(url, db)
    ok, uid, err = client.authenticate(username, password)

    if not ok:
        flash(f"Connection failed: {err}", 'danger')
        return render_template('index.html', products=None)

    session['odoo_authenticated'] = True
    session['odoo_url'] = url
    session['odoo_db'] = db
    session['odoo_uid'] = uid
    session['odoo_cookies'] = client.session.cookies.get_dict()

    ok, products, err = client.get_products()
    if not ok:
        flash(f"Connected but failed to fetch products: {err}", 'danger')
        return render_template('index.html', products=None)

    flash(f"Connexion réussie. UID: {uid}. Produits chargés: {len(products)}.", 'success')
    return render_template('index.html', products=products)