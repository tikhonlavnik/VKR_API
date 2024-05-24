from fastapi import HTTPException, Depends, APIRouter

# from celery_manager import CeleryManager
# from models import Users, get_session, get_current_user

from src.apps.authorization.service import get_current_user
from src.apps.telecom_metrics.schemas import CalculateRequest

# from src.apps.telecom_metrics.service import TelecomService
from src.apps.users.models import Users
from src.celery.managers.telecom_manager import TelecomService


class AuthViews:
    def __init__(self, service: TelecomService):
        self.service = service
        self.router = APIRouter(prefix="/api", tags=["Telecom metrics"])
        self.router.add_api_route(
            "/calculate/latency/", self.calculate_latency, methods=["POST"]
        )
        self.router.add_api_route(
            "/calculate/packet_loss/", self.calculate_packet_loss, methods=["POST"]
        )
        self.router.add_api_route(
            "/calculate/{task_id}/", self.get_result, methods=["GET"]
        )

    async def calculate_latency(
        self,
        request: CalculateRequest,
        # db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(get_current_user),
    ):
        task = await self.service.calculate_latency(
            current_user.id, request.task_name, request.samples
        )
        return task

    async def calculate_packet_loss(
        self,
        request: CalculateRequest,
        # db: AsyncSession = Depends(get_session),
        current_user: Users = Depends(get_current_user),
    ):
        task = await self.service.calculate_packet_loss(
            current_user.id, request.task_name, request.samples
        )
        return task

    async def get_result(self, task_id: str):
        result = await self.service.get_result(task_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"result": result}


telecom_service = TelecomService()
telecom_views = AuthViews(telecom_service)
