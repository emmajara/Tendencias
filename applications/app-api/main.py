import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from flask import Flask, render_template
from Infraestructura.adapters.memoryDB.task_adapter import InMemoryTaskRepository
from Infraestructura.adapters.sqlite_db.task_adapter import SqliteTaskAdapter
from Infraestructura.entry_points.api_rest.task_controller import create_api_rest
from domain.usercase.task.task_usercase import TaskUseCase

def create_app() -> Flask:
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../templates'))
    app = Flask(__name__, template_folder=template_dir)
   
    dict_repo = InMemoryTaskRepository()
    usecase_dict = TaskUseCase(task_repository=dict_repo)
    bp_dict = create_api_rest(task_usecase=usecase_dict, blueprint_name='api_dict')
    app.register_blueprint(bp_dict, url_prefix='/api/dict')

    sqlite_repo = SqliteTaskAdapter()
    usecase_sqlite = TaskUseCase(task_repository=sqlite_repo)
    bp_sqlite = create_api_rest(task_usecase=usecase_sqlite, blueprint_name='api_sqlite')
    app.register_blueprint(bp_sqlite, url_prefix='/api/sqlite')

    @app.route('/', methods=['GET'])
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)