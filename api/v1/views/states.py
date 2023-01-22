#!/usr/bin/python3
"""
    Restful API actions for state
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views('/states', methods=['GET'], 
                strict_slashes=False)
def get_all_states():
    """Retrieve all object states"""
    state_list = []
    for state in storage.all('State').values():
        state_list.append(state.to_dict())
    return jsonify(state_list)

@app_views('/states/<state_id>', methods=['GET'],
                    strict_slashes=False)
def get_state(state_id):
    """Retrieve state by id"""
    try:
        state = storage.get('State', state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)

@app_views('/states/<state_id>', methods=['DELETE'],
                    strict_slashes=False)
def delete_state(state_id):
    """Delete a state through id"""
    try:
        state = storage.get('State', state_id)
        state.delete()
        return jsonify({}),200
    except Exception:
        abort(404)

@app_views('states', methods=['POST'],
                strict_slashes=False)
def create_state():
    """Create a new state"""
    if not request.json:
        abort(400)
        return jsonify({"error":"not a json"})
    if "name" not in request.json:
        abort(400)
        return jsonify({"error":"missing name"})
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()),201

@app_views('states/<state_id>',methods=['PUT'],
                strict_slashes=False)
def update_state(state_id):
    """Update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(404)
        return jsonify({"error":"not a json"})
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
