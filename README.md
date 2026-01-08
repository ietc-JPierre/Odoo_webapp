# Odoo WebApp

Une application **Flask** qui se connecte à un serveur **Odoo** via l’API JSON-RPC.  
Elle permet de s’authentifier et d’afficher uniquement les produits créés par l’utilisateur connecté.

---

##  Structure du projet

odoo-webapp/ 
├── app.py # Point d'entrée Flask 
├── controllers/ # Contrôleurs (routes) 
│ └── home_controller.py 
├── services/ # Services (client Odoo) 
│ └── odoo_client.py 
├── templates/ # Templates Jinja2 
│ ├── index.html 
  └── _layout.html
├── static/ # Fichiers statiques (CSS, JS) 
│ └── css/style.css 
├── requirements.txt # Dépendances Python
└── README.md # Documentation du projet



 Fonctionnalités
Formulaire de connexion à Odoo (URL, base, utilisateur, mot de passe).

Authentification via l’endpoint /web/session/authenticate.

Récupération des produits avec search_read.

Filtrage : seuls les produits créés par l’utilisateur connecté (create_uid = uid) sont affichés.

Tableau des produits avec ID, nom, référence, prix, quantité disponible, catégorie et champs personnalisés (max_guests).

 Dépendances
Flask – Framework web Python.

Requests – Client HTTP pour communiquer avec Odoo.

 Notes
Assure-toi que ton serveur Odoo est démarré et accessible (par défaut : http://localhost:8069/).

Le champ db doit correspondre au nom de ta base Odoo.

Les produits affichés sont uniquement ceux créés par ton utilisateur connecté.
