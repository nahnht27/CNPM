import traceback

from flask import Flask, jsonify
from flask_cors import CORS
from api.swagger import spec
from api.controllers.auth_controller import auth_bp as auth_bp
from api.controllers.user_controller import user_bp

from api.controllers.booking_controller import bp as booking_bp
from api.controllers.category_controller import bp as category_bp
from api.controllers.complaint_controller import bp as complaint_bp
from api.controllers.creative_space_controller import bp as creative_space_bp
from api.controllers.equipment_controller import bp as equipment_bp
from api.controllers.invoice_controller import bp as invoice_bp
from api.controllers.notification_controller import bp as notification_bp
from api.controllers.payment_controller import bp as payment_bp
from api.controllers.post_controller import bp as post_bp
from api.controllers.promotion_controller import bp as promotion_bp
from api.controllers.review_controller import bp as review_bp
from api.controllers.role_controller import bp as role_bp
from api.controllers.service_package_controller import bp as service_package_bp
from api.controllers.service_provider_controller import bp as service_provider_bp
from api.controllers.workshop_controller import bp as workshop_bp

from api.controllers.report_controller import bp as report_bp
from api.controllers.amenity_controller import bp as amenity_bp
from api.controllers.ai_configuration_controller import bp as ai_configuration_bp

from api.middleware import middleware
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Swagger(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(creative_space_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(service_package_bp)
    app.register_blueprint(service_provider_bp)
    app.register_blueprint(workshop_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(amenity_bp)
    app.register_blueprint(ai_configuration_bp)

    # Custom middleware
    middleware(app)

    # CORS for the local frontend (Live Server)
    CORS(
        app,
        resources={r"/*": {
            "origins": [
                "http://127.0.0.1:5500",
                "http://localhost:5500",
                "http://127.0.0.1:3000",
                "http://localhost:3000"
            ]
        }},
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "Accept"],
        supports_credentials=False,
    )

    try:
        init_db(app)
    except Exception:
        traceback.print_exc()

    # Build OpenAPI/Swagger paths
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint in (
                "static",
                "swagger.static",
                "swagger_json",
            ):
                continue

            try:
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)
            except Exception as e:
                print(f"Skip {rule.rule}: {e}")

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    # Swagger UI
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Film Photography Service Platform API"},
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=9999, debug=True)
