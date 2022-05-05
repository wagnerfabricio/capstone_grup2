from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint("categories", __name__, url_prefix="/categories")

# bp.post("/categories")(categories_controller.create_categories)
bp.get("")(categories_controller.retrieve_categories)
bp.get("/<id>")(categories_controller.retrieve_categories_by_id)
# bp.patch("/categories/<id>")(categories_controller.update_category)
# bp.delete("/categories/<id>")(categories_controller.delete_category)
