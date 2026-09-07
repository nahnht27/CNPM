from src.api.controllers.auth_controller import auth_bp
from src.api.controllers.booking_controller import bp as booking_bp
from src.api.controllers.category_controller import bp as category_bp
from src.api.controllers.complaint_controller import bp as complaint_bp
from src.api.controllers.creative_space_controller import bp as creative_space_bp
from src.api.controllers.equipment_controller import bp as equipment_bp
from src.api.controllers.amenity_controller import bp as amenity_bp
from src.api.controllers.invoice_controller import bp as invoice_bp
from src.api.controllers.notification_controller import bp as notification_bp
from src.api.controllers.payment_controller import bp as payment_bp
from src.api.controllers.post_controller import bp as post_bp
from src.api.controllers.promotion_controller import bp as promotion_bp
from src.api.controllers.review_controller import bp as review_bp
from src.api.controllers.role_controller import bp as role_bp
from src.api.controllers.service_package_controller import bp as service_package_bp
from src.api.controllers.service_session_controller import bp as service_session_bp
from src.api.controllers.service_provider_controller import bp as service_provider_bp
from src.api.controllers.report_controller import bp as report_bp
from src.api.controllers.workshop_controller import bp as workshop_bp


def register_routes(app):

    app.register_blueprint(auth_bp)

    app.register_blueprint(role_bp)
    app.register_blueprint(service_provider_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(amenity_bp) 
    app.register_blueprint(creative_space_bp)
    app.register_blueprint(equipment_bp)

    app.register_blueprint(booking_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(report_bp) 

    app.register_blueprint(service_package_bp)
    app.register_blueprint(service_session_bp)
    app.register_blueprint(promotion_bp)

    app.register_blueprint(post_bp)
    app.register_blueprint(workshop_bp)

    app.register_blueprint(notification_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(review_bp)