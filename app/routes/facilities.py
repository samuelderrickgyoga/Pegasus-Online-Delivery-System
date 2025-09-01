from flask import Blueprint, request, jsonify
from models.facility import Facility

facilities_bp = Blueprint("facilities", __name__, url_prefix="/api/facilities")


# Basic CRUD

@facilities_bp.route("/", methods=["GET"])
def get_all_facilities():
    """List all facilities with optional search/filter"""
    facility_type = request.args.get("type")
    partner = request.args.get("partner")
    capability = request.args.get("capability")
    location = request.args.get("location")

    if facility_type:
        facilities = Facility.get_by_type(facility_type)
    elif partner:
        facilities = Facility.get_by_partner(partner)
    elif capability:
        facilities = Facility.search_by_capability(capability)
    elif location:
        facilities = Facility.get_by_location(location)
    else:
        facilities = Facility.get_all()

    return jsonify([f.to_dict() for f in facilities]), 200


@facilities_bp.route("/<int:facility_id>", methods=["GET"])
def get_facility_by_id(facility_id):
    """View facility details"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    return jsonify(facility.to_dict(include_related=True)), 200


@facilities_bp.route("/", methods=["POST"])
def create_facility():
    """Create new facility"""
    data = request.get_json()
    try:
        facility = Facility.create(
            name=data["name"],
            location=data.get("location"),
            description=data.get("description"),
            partner_org=data.get("partner_org"),
            facility_type=data.get("facility_type"),
            capabilities=data.get("capabilities"),
        )
        return jsonify(facility.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@facilities_bp.route("/<int:facility_id>", methods=["PUT"])
def update_facility(facility_id):
    """Edit facility details"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    try:
        updated = facility.update(**request.get_json())
        return jsonify(updated.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@facilities_bp.route("/<int:facility_id>", methods=["DELETE"])
def delete_facility(facility_id):
    """Delete facility"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    try:
        facility.delete()
        return jsonify({"message": "Facility deleted successfully"}), 200
    except ValueError as ve:
        # Custom error when facility has associated projects
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------------
# Related entity routes
# ------------------------------

@facilities_bp.route("/<int:facility_id>/services", methods=["GET"])
def get_services_by_facility(facility_id):
    """List services offered by facility"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    return jsonify([s.to_dict() for s in facility.services]), 200


@facilities_bp.route("/<int:facility_id>/equipment", methods=["GET"])
def get_equipment_by_facility(facility_id):
    """List equipment at facility"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    return jsonify([e.to_dict() for e in facility.equipment]), 200


@facilities_bp.route("/<int:facility_id>/projects", methods=["GET"])
def get_projects_by_facility(facility_id):
    """List projects at facility"""
    facility = Facility.get_by_id(facility_id)
    if not facility:
        return jsonify({"error": "Facility not found"}), 404
    return jsonify([p.to_dict() for p in facility.projects]), 200
