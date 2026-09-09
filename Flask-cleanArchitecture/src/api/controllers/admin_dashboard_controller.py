from flask import Blueprint, jsonify
from sqlalchemy import func

from infrastructure.databases.postgres import session

from infrastructure.models.user_model import UserModel
from infrastructure.models.service_provider_model import ServiceProviderModel
from infrastructure.models.booking_model import BookingModel
from infrastructure.models.complaint_model import ComplaintModel
from infrastructure.models.payment_model import PaymentModel
from infrastructure.models.invoice_model import InvoiceModel
from infrastructure.models.category_model import CategoryModel


bp = Blueprint(
    "admin_dashboard",
    __name__,
    url_prefix="/admin"
)


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Get overview statistics for Admin Dashboard.
    """

    revenue = (
        session.query(
            func.coalesce(
                func.sum(
                    InvoiceModel.total_amount
                ),
                0
            )
        )
        .scalar()
        or 0
    )


    pending_providers = (
        session.query(
            func.count(
                ServiceProviderModel.id
            )
        )
        .filter(
            func.lower(
                ServiceProviderModel.verification_status
            ) == "pending"
        )
        .scalar()
        or 0
    )


    total_users = (
        session.query(
            func.count(
                UserModel.ID
            )
        )
        .scalar()
        or 0
    )


    total_providers = (
        session.query(
            func.count(
                ServiceProviderModel.id
            )
        )
        .scalar()
        or 0
    )


    total_bookings = (
        session.query(
            func.count(
                BookingModel.id
            )
        )
        .scalar()
        or 0
    )


    total_complaints = (
        session.query(
            func.count(
                ComplaintModel.id
            )
        )
        .scalar()
        or 0
    )


    total_payments = (
        session.query(
            func.count(
                PaymentModel.id
            )
        )
        .scalar()
        or 0
    )


    total_invoices = (
        session.query(
            func.count(
                InvoiceModel.id
            )
        )
        .scalar()
        or 0
    )


    total_categories = (
        session.query(
            func.count(
                CategoryModel.id
            )
        )
        .scalar()
        or 0
    )


    return jsonify(
        {
            "total_users": total_users,
            "total_providers": total_providers,
            "pending_providers": pending_providers,
            "total_bookings": total_bookings,
            "total_complaints": total_complaints,
            "total_payments": total_payments,
            "total_invoices": total_invoices,
            "total_categories": total_categories,
            "total_revenue": float(revenue),
        }
    ), 200