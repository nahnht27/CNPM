import traceback
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from services.equipment_service import EquipmentService
from infrastructure.repositories.equipment_repository import EquipmentRepository
from api.schemas.equipment import EquipmentRequestSchema, EquipmentResponseSchema
from config import DevelopmentConfig

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

# Tự khởi tạo Engine và Scoped Session riêng cho module Equipment
# Giải quyết triệt để lỗi Concurrent Session mà KHÔNG CẦN sửa file mssql.py hay postgres.py chung
engine = create_engine(DevelopmentConfig.DATABASE_URI, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

request_schema = EquipmentRequestSchema()
response_schema = EquipmentResponseSchema()


def get_equipment_service(db_session):
    """Khởi tạo service với db session riêng cho từng request."""
    return EquipmentService(EquipmentRepository(db_session))


@bp.route('/', methods=['GET'])
def list_equipment():
    """
    List equipment
    ---
    get:
      summary: Lấy danh sách thiết bị
      tags:
        - Equipment
      parameters:
        - name: space_id
          in: query
          required: false
          schema:
            type: integer
          description: Lọc thiết bị theo ID không gian
      responses:
        200:
          description: Danh sách thiết bị
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/EquipmentResponse'
    """
    db_session = SessionLocal()
    try:
        service = get_equipment_service(db_session)
        space_id = request.args.get('space_id', type=int)

        if space_id and hasattr(service, 'list_by_space'):
            items = service.list_by_space(space_id)
        elif space_id and hasattr(service, 'list_equipment'):
            items = service.list_equipment(space_id=space_id)
        else:
            items = service.list_equipment()

        return jsonify(response_schema.dump(items, many=True)), 200

    except Exception as e:
        print("\n================ [EQUIPMENT LOG ERROR] ================")
        traceback.print_exc()
        print("=======================================================\n")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    finally:
        db_session.close()
        SessionLocal.remove()


@bp.route('/<int:eq_id>', methods=['GET'])
def get_equipment(eq_id):
    """
    Get equipment
    ---
    get:
      summary: Lấy chi tiết thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Chi tiết thiết bị
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        404:
          description: Không tìm thấy thiết bị
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    db_session = SessionLocal()
    try:
        service = get_equipment_service(db_session)
        item = service.get_equipment(eq_id)

        if not item:
            return jsonify({'message': 'Equipment not found'}), 404

        return jsonify(response_schema.dump(item)), 200

    except Exception as e:
        print("\n================ [EQUIPMENT LOG ERROR] ================")
        traceback.print_exc()
        print("=======================================================\n")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    finally:
        db_session.close()
        SessionLocal.remove()


@bp.route('/', methods=['POST'])
def create_equipment():
    """
    Create equipment
    ---
    post:
      summary: Tạo thiết bị mới
      tags:
        - Equipment
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EquipmentRequest'
      responses:
        201:
          description: Thiết bị đã được tạo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    db_session = SessionLocal()
    try:
        data = request.get_json()
        errors = request_schema.validate(data)

        if errors:
            return jsonify(errors), 400

        service = get_equipment_service(db_session)
        item = service.create_equipment(**data)
        db_session.commit()

        return jsonify(response_schema.dump(item)), 201

    except Exception as e:
        db_session.rollback()
        print("\n================ [EQUIPMENT LOG ERROR] ================")
        traceback.print_exc()
        print("=======================================================\n")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    finally:
        db_session.close()
        SessionLocal.remove()


@bp.route('/<int:eq_id>', methods=['PUT'])
def update_equipment(eq_id):
    """
    Update equipment
    ---
    put:
      summary: Cập nhật thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/EquipmentRequest'
      responses:
        200:
          description: Thiết bị đã được cập nhật
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/EquipmentResponse'
        400:
          description: Dữ liệu không hợp lệ
    """
    db_session = SessionLocal()
    try:
        data = request.get_json()
        errors = request_schema.validate(data)

        if errors:
            return jsonify(errors), 400

        service = get_equipment_service(db_session)
        item = service.update_equipment(eq_id, **data)
        db_session.commit()

        return jsonify(response_schema.dump(item)), 200

    except Exception as e:
        db_session.rollback()
        print("\n================ [EQUIPMENT LOG ERROR] ================")
        traceback.print_exc()
        print("=======================================================\n")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    finally:
        db_session.close()
        SessionLocal.remove()


@bp.route('/<int:eq_id>', methods=['DELETE'])
def delete_equipment(eq_id):
    """
    Delete equipment
    ---
    delete:
      summary: Xóa thiết bị
      tags:
        - Equipment
      parameters:
        - name: eq_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Đã xóa thành công
    """
    db_session = SessionLocal()
    try:
        service = get_equipment_service(db_session)
        service.delete_equipment(eq_id)
        db_session.commit()

        return '', 204

    except Exception as e:
        db_session.rollback()
        print("\n================ [EQUIPMENT LOG ERROR] ================")
        traceback.print_exc()
        print("=======================================================\n")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
    finally:
        db_session.close()
        SessionLocal.remove()