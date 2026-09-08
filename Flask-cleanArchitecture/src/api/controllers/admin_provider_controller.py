from datetime import datetime

from flask import Blueprint, jsonify

from infrastructure.databases.postgres import session
from infrastructure.models.service_provider_model import ServiceProviderModel
from infrastructure.models.user_model import UserModel


bp = Blueprint(
    'admin_provider',
    __name__,
    url_prefix='/admin/providers'
)



@bp.route('', methods=['GET'])
def list_providers():
    providers = (
        session.query(ServiceProviderModel)
        .order_by(ServiceProviderModel.created_at.desc())
        .all()
    )

    result = []

    for provider in providers:
        user = (
            session.query(UserModel)
            .filter(UserModel.ID == provider.user_id)
            .first()
        )

        result.append({
            'id': provider.id,
            'user_id': provider.user_id,
            'business_name': provider.business_name,
            'tax_code': provider.tax_code,
            'business_address': provider.business_address,
            'license_url': provider.license_url,
            'verification_status': provider.verification_status,
            'approved_at': (
                provider.approved_at.isoformat()
                if provider.approved_at
                else None
            ),
            'created_at': (
                provider.created_at.isoformat()
                if provider.created_at
                else None
            ),
            'full_name': user.full_name if user else None,
            'email': user.email if user else None,
            'phone': user.phone if user else None,
            'user_status': user.status if user else None
        })

    return jsonify(result), 200
@bp.route('/<int:provider_id>/approve', methods=['PUT'])
def approve_provider(provider_id):
    provider = (
        session.query(ServiceProviderModel)
        .filter(ServiceProviderModel.id == provider_id)
        .first()
    )

    if not provider:
        return jsonify({
            'message': 'Provider not found'
        }), 404

    if provider.verification_status == 'approved':
        return jsonify({
            'message': 'Provider has already been approved'
        }), 400

    user = (
        session.query(UserModel)
        .filter(UserModel.ID == provider.user_id)
        .first()
    )

    if not user:
        return jsonify({
            'message': 'Provider user not found'
        }), 404

    now = datetime.now()

    provider.verification_status = 'approved'
    provider.approved_at = now

    user.status = 'active'

    try:
        session.commit()
    except Exception:
        session.rollback()

        return jsonify({
            'message': 'Unable to approve provider'
        }), 500

    return jsonify({
        'message': 'Provider approved successfully',
        'provider_id': provider.id,
        'verification_status': provider.verification_status,
        'user_status': user.status,
        'approved_at': now.isoformat()
    }), 200