from skeleton_python_system import create_app
from skeleton_python_system.blueprints.index import INDEX_BLUEPRINT

if __name__ == "__main__":
    APP = create_app()
    APP.register_blueprint(INDEX_BLUEPRINT)

    @APP.errorhandler(404)
    @APP.errorhandler(405)
    def _handle_api_error(ex):
        if request.path.startswith("/api/"):
            return jsonify_error(ex)

        return ex

    APP.run(port=45000, host="0.0.0.0")
