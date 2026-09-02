from flask import request, jsonify


ALLOWED_ORIGINS = {
    "http://127.0.0.1:5500",
    "http://localhost:5500",
}


def log_request_info(app):
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())


def error_handling_middleware(error):
    response = jsonify({"error": str(error)})
    response.status_code = 500
    return response


def add_custom_headers(response):
    origin = request.headers.get("Origin")

    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Accept, Authorization"
        )
        response.headers["Access-Control-Max-Age"] = "3600"

    response.headers["X-Custom-Header"] = "Value"

    return response


def middleware(app):

    @app.before_request
    def before_request():
        log_request_info(app)

        # Handle CORS preflight request
        if request.method == "OPTIONS":
            return "", 204

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return error_handling_middleware(error)