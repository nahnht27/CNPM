class ReportService:
    def __init__(self, report_repository):
        self.report_repository = report_repository

    def get_revenue_report(self, from_date, to_date, provider_id=None):
        total_revenue = self.report_repository.get_total_revenue(
            from_date, to_date, provider_id
        )
        revenue_by_month = self.report_repository.get_revenue_by_month(
            from_date, to_date, provider_id
        )
        total_bookings = self.report_repository.get_total_bookings(
            from_date, to_date, provider_id
        )
        total_invoices = self.report_repository.get_total_invoices(
            from_date, to_date, provider_id
        )

        return {
            'from_date': from_date,
            'to_date': to_date,
            'provider_id': provider_id,
            'total_revenue': total_revenue,
            'total_bookings': total_bookings,
            'total_invoices': total_invoices,
            'revenue_by_month': revenue_by_month,
        }