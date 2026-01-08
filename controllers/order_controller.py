from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from services.odoo_client import OdooClient

order_bp = Blueprint("order", __name__)


def get_odoo_client_from_session():
    if not session.get("odoo_authenticated"):
        return None

    base_url = session.get("odoo_url")
    db = session.get("odoo_db")
    cookies = session.get("odoo_cookies", {})

    client = OdooClient(base_url, db)
    client.session.cookies.update(cookies)
    return client


@order_bp.route("/order/new", methods=["GET"])
def new_order_form():
    client = get_odoo_client_from_session()
    if client is None:
        flash("Veuillez d'abord vous connecter à Odoo.", "danger")
        return redirect(url_for("home.index"))

    ok_p, partners, err_p = client.get_partners(limit=50)
    if not ok_p:
        partners = []
        flash(f"Impossible de charger les clients: {err_p}", "danger")

    ok_prod, products, err_prod = client.get_products(limit=50)
    if not ok_prod:
        products = []
        flash(f"Impossible de charger les produits: {err_prod}", "danger")

    return render_template("order_form.html", partners=partners, products=products)


@order_bp.route("/order/create", methods=["POST"])
def create_order():
    client = get_odoo_client_from_session()
    if client is None:
        flash("Session Odoo expirée, veuillez vous reconnecter.", "danger")
        return redirect(url_for("home.index"))

    try:
        partner_id = int(request.form["partner_id"])
        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])
        price_unit = float(request.form["price_unit"])
    except Exception:
        flash("Veuillez remplir correctement tous les champs.", "danger")
        return redirect(url_for("order.new_order_form"))

   
    ok, order_id, err = client.create_order(partner_id)
    if not ok:
        flash(f"Erreur création commande : {err}", "danger")
        return redirect(url_for("order.new_order_form"))

    
    ok, line_id, err = client.add_order_line(order_id, product_id, quantity, price_unit)
    if not ok:
        flash(f"Erreur ajout ligne : {err}", "danger")
        return redirect(url_for("order.new_order_form"))

    
    ok, status, err = client.get_order_status(order_id)
    if not ok:
        flash(f"Erreur récupération statut : {err}", "danger")
        return redirect(url_for("order.new_order_form"))

    return render_template("order_status.html", order_id=order_id, status=status)


@order_bp.route("/partners/list")
def partners_list():
    client = get_odoo_client_from_session()
    if client is None:
        flash("Veuillez d'abord vous connecter à Odoo.", "danger")
        return redirect(url_for("home.index"))

    ok, partners, err = client.get_partners(limit=100)
    if not ok:
        flash(f"Erreur chargement clients : {err}", "danger")
        partners = []

    return render_template("partners_list.html", partners=partners)