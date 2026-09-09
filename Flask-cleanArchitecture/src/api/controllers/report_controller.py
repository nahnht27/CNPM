from xml.parsers.expat import errors

from flask import Blueprint, request, jsonify
from services.report_service import ReportService
from infrastructure.repositories.report_repository import ReportRepository
from api.schemas.report import RevenueReportRequestSchema, RevenueReportResponseSchema
from infrastructure.databases.postgres import session

bp = Blueprint('report', __name__, url_prefix='/reports')

report_service = ReportService(ReportRepository(session))

request_schema = RevenueReportRequestSchema()
response_schema = RevenueReportResponseSchema()


@bp.route('/provider', methods=['GET'])
def get_provider_revenue_report():
    """
    Provider revenue report
    ---
    get:
      summary: UC23 - Provider xem báo cáo doanh thu
      tags:
        - Report
      parameters:
        - name: provider_id
          in: query
          required: true
          schema:
            type: integer
        - name: from_date
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: to_date
          in: query
          required: true
          schema:
            type: string
            format: date-time
      responses:
        200:
          description: Báo cáo doanh thu của provider
        400:
          description: Thiếu tham số bắt buộc
    """
    provider_id = request.args.get('provider_id', type=int)
    if provider_id is None:
        return jsonify({'message': 'provider_id is required'}), 400

    report_data = {
    'from_date': request.args.get('from_date'),
    'to_date': request.args.get('to_date')
    }
    errors = request_schema.validate(report_data)
    if errors:return jsonify(errors), 400
    data = request_schema.load(report_data)
    report = report_service.get_revenue_report(
        from_date=data['from_date'],
        to_date=data['to_date'],
        provider_id=provider_id,
    )
    return jsonify(response_schema.dump(report)), 200


@bp.route('/system', methods=['GET'])
def get_system_revenue_report():
    """
    System-wide revenue report
    ---
    get:
      summary: UC34 - Admin xem báo cáo toàn hệ thống
      tags:
        - Report
      parameters:
        - name: from_date
          in: query
          required: true
          schema:
            type: string
            format: date-time
        - name: to_date
          in: query
          required: true
          schema:
            type: string
            format: date-time
      responses:
        200:
          description: Báo cáo doanh thu toàn hệ thống
        400:
          description: Thiếu tham số bắt buộc
    """
    report_data = {
    'from_date': request.args.get('from_date'),
    'to_date': request.args.get('to_date')
    }
    errors = request_schema.validate(report_data) 
    if errors:return jsonify(errors), 400
    data = request_schema.load(report_data)
    report = report_service.get_revenue_report(
        from_date=data['from_date'],
        to_date=data['to_date'],
        provider_id=None,
    )
    return jsonify(response_schema.dump(report)), 200