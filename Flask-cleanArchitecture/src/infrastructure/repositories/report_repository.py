from sqlalchemy import func
from infrastructure.models.payment_model import PaymentModel
from infrastructure.models.invoice_model import InvoiceModel
from infrastructure.models.service_session_model import ServiceSessionModel
from infrastructure.models.booking_model import BookingModel
from infrastructure.models.creative_space_model import CreativeSpaceModel


class ReportRepository:
    def __init__(self, session):
        self.session = session

    def get_revenue_query(self, from_date, to_date, provider_id=None):
        """
        JOIN chuỗi: Payments -> Invoices -> ServiceSessions -> Bookings -> CreativeSpaces
        provider_id = None -> không lọc (UC34 - toàn hệ thống)
        provider_id = <id> -> lọc theo Provider (UC23)
        """
        query = (
            self.session.query(PaymentModel)
            .join(InvoiceModel, PaymentModel.invoice_id == InvoiceModel.id)
            .join(ServiceSessionModel, InvoiceModel.session_id == ServiceSessionModel.id)
            .join(BookingModel, ServiceSessionModel.booking_id == BookingModel.id)
            .join(CreativeSpaceModel, BookingModel.space_id == CreativeSpaceModel.id)
            .filter(PaymentModel.paid_at >= from_date)
            .filter(PaymentModel.paid_at <= to_date)
            .filter(PaymentModel.status == 'completed')
        )
        if provider_id is not None:
            query = query.filter(CreativeSpaceModel.provider_id == provider_id)
        return query

    def get_total_revenue(self, from_date, to_date, provider_id=None):
        query = self.get_revenue_query(from_date, to_date, provider_id)
        total = query.with_entities(func.sum(PaymentModel.amount)).scalar()
        return total or 0

    def get_revenue_by_month(self, from_date, to_date, provider_id=None):
        query = self.get_revenue_query(from_date, to_date, provider_id)
        results = (
            query.with_entities(
                func.to_char(PaymentModel.paid_at, 'YYYY-MM').label('month'),
                func.sum(PaymentModel.amount).label('total'),
            )
            .group_by('month')
            .order_by('month')
            .all()
        )
        return {row.month: float(row.total) for row in results}

    def get_total_bookings(self, from_date, to_date, provider_id=None):
        query = (
            self.session.query(BookingModel)
            .join(CreativeSpaceModel, BookingModel.space_id == CreativeSpaceModel.id)
            .filter(BookingModel.created_at >= from_date)
            .filter(BookingModel.created_at <= to_date)
        )
        if provider_id is not None:
            query = query.filter(CreativeSpaceModel.provider_id == provider_id)
        return query.count()

    def get_total_invoices(self, from_date, to_date, provider_id=None):
        query = (
            self.session.query(InvoiceModel)
            .join(ServiceSessionModel, InvoiceModel.session_id == ServiceSessionModel.id)
            .join(BookingModel, ServiceSessionModel.booking_id == BookingModel.id)
            .join(CreativeSpaceModel, BookingModel.space_id == CreativeSpaceModel.id)
            .filter(InvoiceModel.issued_at >= from_date)
            .filter(InvoiceModel.issued_at <= to_date)
        )
        if provider_id is not None:
            query = query.filter(CreativeSpaceModel.provider_id == provider_id)
        return query.count()