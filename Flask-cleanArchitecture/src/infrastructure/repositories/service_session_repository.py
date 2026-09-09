from typing import List, Optional

from infrastructure.models.service_session_model import ServiceSessionModel


class ServiceSessionRepository:

    def __init__(self, session):
        self.session = session

    # ==========================================================
    # CREATE
    # ==========================================================

    def add(self, data) -> ServiceSessionModel:

        model = ServiceSessionModel(
            booking_id=data.get('booking_id'),
            check_in_time=data.get('check_in_time'),
            check_out_time=data.get('check_out_time'),
            check_in_method=data.get('check_in_method'),
            actual_duration_minutes=data.get(
                'actual_duration_minutes'
            ),
            notes=data.get('notes'),
            status=data.get('status', 'pending')
        )

        try:
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)

            return model

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # GET BY ID
    # ==========================================================

    def get_by_id(
        self,
        session_id: int
    ) -> Optional[ServiceSessionModel]:

        return (
            self.session.query(ServiceSessionModel)
            .filter(
                ServiceSessionModel.id == session_id
            )
            .first()
        )

    # ==========================================================
    # GET BY BOOKING
    # ==========================================================

    def get_by_booking_id(
        self,
        booking_id: int
    ) -> Optional[ServiceSessionModel]:

        return (
            self.session.query(ServiceSessionModel)
            .filter(
                ServiceSessionModel.booking_id == booking_id
            )
            .first()
        )

    # ==========================================================
    # GET ALL
    # ==========================================================

    def list(self) -> List[ServiceSessionModel]:

        return (
            self.session
            .query(ServiceSessionModel)
            .all()
        )

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(
        self,
        session_id: int,
        data: dict
    ) -> Optional[ServiceSessionModel]:

        model = self.get_by_id(session_id)

        if not model:
            return None

        try:

            for key, value in data.items():

                if hasattr(model, key):
                    setattr(model, key, value)

            self.session.commit()
            self.session.refresh(model)

            return model

        except Exception:
            self.session.rollback()
            raise

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(
        self,
        session_id: int
    ) -> bool:

        model = self.get_by_id(session_id)

        if not model:
            return False

        try:

            self.session.delete(model)
            self.session.commit()

            return True

        except Exception:
            self.session.rollback()
            raise