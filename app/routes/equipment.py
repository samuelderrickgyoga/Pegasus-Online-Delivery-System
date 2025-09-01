from flask import Blueprint, request, jsonify
from models.equipment import Equipment

equipment_bp = Blueprint("equipment", __name__, url_prefix="/api/equipment")

# ------------------------------
# Basic CRUD
# ------------------------------

@equipment_bp.route("/", methods=["GET"])
def get_all_equipment():
    """List all equipment globally with optional filters"""
    usage_domain = request.args.get("usageDomain")
    support_phase = request.args.get("supportPhase")
    facility_id = request.args.get("facilityId", type=int)
    capability = request.args.get("capability")

    if usage_domain:
        equipment = Equipment.get_by_domain(usage_domain)
    elif support_phase:
        equipment = Equipment.get_by_phase(support_phase)
    elif facility_id:
        equipment = Equipment.get_by_facility(facility_id)
    elif capability:
        equipment = Equipment.search_by_capability(capability)
    else:
        equipment = Equipment.get_all()

    return jsonify([eq.to_dict(include_facility_info=True) for eq in equipment]), 200


@equipment_bp.route("/search", methods=["GET"])
def search_equipment():
    """Search equipment by query across name, description, or capabilities"""
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing search query"}), 400

    results = Equipment.search_equipment(query)
    return jsonify([eq.to_dict(include_facility_info=True) for eq in results]), 200


@equipment_bp.route("/<int:equipment_id>", methods=["GET"])
def get_equipment_by_id(equipment_id):
    """View equipment details"""
    equipment = Equipment.get_by_id(equipment_id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    return jsonify(equipment.to_dict(include_facility_info=True, include_related=True)), 200


@equipment_bp.route("/", methods=["POST"])
def create_equipment():
    """Create new equipment"""
    data = request.get_json()
    try:
        equipment = Equipment.create(
            facility_id=data["facility_id"],
            name=data["name"],
            capabilities=data.get("capabilities"),
            description=data.get("description"),
            inventory_code=data.get("inventory_code"),
            usage_domain=data.get("usage_domain"),
            support_phase=data.get("support_phase"),
        )
        return jsonify(equipment.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@equipment_bp.route("/<int:equipment_id>", methods=["PUT"])
def update_equipment(equipment_id):
    """Edit equipment details"""
    equipment = Equipment.get_by_id(equipment_id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    try:
        updated = equipment.update(**request.get_json())
        return jsonify(updated.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@equipment_bp.route("/<int:equipment_id>", methods=["DELETE"])
def delete_equipment(equipment_id):
    """Delete equipment"""
    equipment = Equipment.get_by_id(equipment_id)
    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404
    try:
        equipment.delete()
        return jsonify({"message": "Equipment deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
