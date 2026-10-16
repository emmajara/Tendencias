from flask import Blueprint, request, jsonify
from dataclasses import asdict
from domain.usercase.task.task_usercase import TaskUseCase

def create_api_rest(task_usecase: TaskUseCase, blueprint_name: str) -> Blueprint:
    bp = Blueprint(blueprint_name, __name__)

    @bp.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = task_usecase.get_all_tasks()
        return jsonify([asdict(task) for task in tasks]), 200

    @bp.route('/tasks', methods=['POST'])
    def create_task():
        data = request.get_json() or {}
        try:
            task = task_usecase.create_task(data.get('title', ''))
            return jsonify(asdict(task)), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @bp.route('/tasks/<int:task_id>/complete', methods=['PUT'])
    def complete_task(task_id: int):
        try:
            task = task_usecase.complete_task(task_id)
            return jsonify(asdict(task)), 200
        except LookupError as e:
            return jsonify({"error": str(e)}), 404

    return bp