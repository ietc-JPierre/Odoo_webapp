from flask import Blueprint, request, render_template, redirect, url_for, flash
from services.odoo_client import OdooClient

order_bp = Blueprint("order", __name__)

# ✅ Client Odoo (adapter base_url et db si besoin)
odoo = OdooClient(
    base_url="http://localhost:8069",
    db="odoo_dev"
)

# ---------------------------------------------------------
# ✅ FORMULAIRE DE CRÉATION DE COMMANDE
# ---------------------------------------------------------
@order_bp.route("/order/new", methods=["GET"])
def new_order_form():
    return render_template("order_form.html")


# ---------------------------------------------------------
# ✅ TRAITEMENT : CRÉER LA COMMANDE + AJOUTER LA LIGNE
# ---------------------------------------------------------
@order_bp.route("/order/create", methods=["POST"])
def create_order():
    try:
        partner_id = int(request.form["partner_id"])
        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])
        price_unit = float(request.form["price_unit"])
    except Exception:
        flash("Veuillez remplir correctement tous les champs.", "danger")
        return redirect(url_for("order.new_order_form"))

    # ✅ 1) Créer la commande
    success, order_id, error = odoo.create_order(partner_id)
    if not success:
        flash(f"Erreur création commande : {error}", "danger")
        return redirect(url_for("order.new_order_form"))

    # ✅ 2) Ajouter une ligne
    success, line_id, error = odoo.add_order_line(order_id, product_id, quantity, price_unit)
    if not success:
        flash(f"Erreur ajout ligne : {error}", "danger")
        return redirect(url_for("order.new_order_form"))

    # ✅ 3) Récupérer le statut
    success, status, error = odoo.get_order_status(order_id)
    if not success:
        flash(f"Erreur récupération statut : {error}", "danger")
        return redirect(url_for("order.new_order_form"))

    # ✅ 4) Afficher la page de statut
    return render_template("order_status.html", order_id=order_id, status=status)


# ---------------------------------------------------------
# ✅ LISTE DES CLIENTS (optionnel)
# ---------------------------------------------------------
@order_bp.route("/partners")
def list_partners():
    partners = odoo.get_partners(limit=10)
    return {"partners": partners}


# ---------------------------------------------------------
# ✅ LISTE DES PRODUITS (optionnel)
# ---------------------------------------------------------
@order_bp.route("/products")
def list_products():
    success, products, error = odoo.get_products()
    if not success:
        return {"error": error}
    return {"products": products}