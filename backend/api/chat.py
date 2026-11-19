
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.database.models import (
    ChatSession
)

from backend.database.schemas import (
    ChatSessionCreate,
    ChatSessionRead,
    ChatMessageRequest,
    ChatTurnResponse
)

from backend.security.authentication import (
    get_current_customer
)

from backend.services.chat_service import (
    create_chat_session,
    process_chat_message
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


# =========================================================
# CREATE CHAT SESSION
# =========================================================

@router.post(
    "/sessions",
    response_model=ChatSessionRead
)
def create_session(
    request: ChatSessionCreate,
    current_customer=Depends(get_current_customer),
    db: Session = Depends(get_db)
):

    return create_chat_session(
        db=db,
        customer_id=current_customer.id,
        session_title=request.session_title
    )


# =========================================================
# GET CUSTOMER CHAT SESSIONS
# =========================================================

@router.get(
    "/sessions",
    response_model=list[ChatSessionRead]
)
def get_customer_sessions(
    current_customer=Depends(get_current_customer),
    db: Session = Depends(get_db)
):

    statement = (
        select(ChatSession)
        .where(
            ChatSession.customer_id == current_customer.id
        )
        .order_by(ChatSession.created_at.desc())
    )

    return db.scalars(statement).all()


# =========================================================
# SEND CHAT MESSAGE
# =========================================================

@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatTurnResponse
)
def send_message(
    session_id: str,
    request: ChatMessageRequest,
    current_customer=Depends(get_current_customer),
    db: Session = Depends(get_db)
):

    return process_chat_message(
        db=db,
        session_id=session_id,
        customer_id=current_customer.id,
        message=request.content
    )
