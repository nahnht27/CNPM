from flask import Blueprint, request, jsonify

from services.ai_service import AIService
from infrastructure.repositories.ai_interaction_log_repository import (
    AIInteractionLogRepository
)
from api.schemas.ai_interaction_log import (
    AIInteractionLogRequestSchema,
    AIInteractionLogResponseSchema
)
from infrastructure.databases.mssql import session


bp = Blueprint('ai', __name__, url_prefix='/ai')


ai_service = AIService(
    AIInteractionLogRepository(session)
)

request_schema = AIInteractionLogRequestSchema()
response_schema = AIInteractionLogResponseSchema()


@bp.route('/ask', methods=['POST'])
def ask_ai():
    """
    Ask AI assistant
    ---
    post:
      summary: Đặt câu hỏi và nhận phản hồi từ trợ lý AI
      tags:
        - AI
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AIInteractionLogRequest'
      responses:
        200:
          description: AI trả lời thành công
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AIInteractionLogResponse'
        400:
          description: Dữ liệu không hợp lệ
        500:
          description: Lỗi khi gọi AI API
    """

    data = request.get_json()

    if not data:
        return jsonify({
            'message': 'Request data is required'
        }), 400

    errors = request_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        result = ai_service.ask_ai(**data)

        return jsonify(
            response_schema.dump(result)
        ), 200

    except ValueError as e:
        return jsonify({
            'message': str(e)
        }), 400

    except Exception:
        return jsonify({
            'message': 'Unable to process AI request'
        }), 500