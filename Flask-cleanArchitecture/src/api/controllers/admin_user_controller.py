from flask import Blueprint, jsonify

from infrastructure.databases.postgres import session
from infrastructure.models.user_model import UserModel
from infrastructure.models.service_provider_model import ServiceProviderModel


bp = Blueprint(
    'admin_user',
    __name__,
    url_prefix='/admin/users'
)


@bp.route('', methods=['GET'])
def list_users():
    users = (
        session.query(UserModel)
        .order_by(UserModel.created_at.desc())
        .all()
    )

    result = []

    for user in users:
        provider = (
            session.query(ServiceProviderModel)
            .filter(
                ServiceProviderModel.user_id == user.ID
            )
            .first()
        )

        result.append({
            'user_id': user.ID,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'phone': user.phone,
            'avatar': user.avatar,
            'gender': user.gender,
            'created_at': (
                user.created_at.isoformat()
                if user.created_at
                else None
            ),
            'status': user.status,
            'role_id': user.role_id,

            'is_provider': provider is not None,

            'provider': (
                {
                    'id': provider.id,
                    'business_name': provider.business_name,
                    'tax_code': provider.tax_code,
                    'business_address': provider.business_address,
                    'license_url': provider.license_url,
                    'verification_status':
                        provider.verification_status,
                    'approved_at': (
                        provider.approved_at.isoformat()
                        if provider.approved_at
                        else None
                    )
                }
                if provider
                else None
            )
        })

    return jsonify(result), 200