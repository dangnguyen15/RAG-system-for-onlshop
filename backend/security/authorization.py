
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from backend.database.models import (
    ChatSession,
    Order,
    KnowledgeDocument
)


# =========================================================
# VERIFY CHAT SESSION OWNERSHIP
# =========================================================

def get_owned_chat_session(
    db: Session,
    session_id: str,
    customer_id: str
):

    session = db.scalar(
        select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.customer_id == customer_id
        )
    )

    if session is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found."
        )

    return session


# =========================================================
# VERIFY ORDER OWNERSHIP
# =========================================================

def get_owned_order(
    db: Session,
    order_code: str,
    customer_id: str
):

    order = db.scalar(
        select(Order).where(
            Order.order_code == order_code,
            Order.customer_id == customer_id
        )
    )

    if order is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    return order


# =========================================================
# VERIFY KNOWLEDGE DOCUMENT ACCESS
# =========================================================

def get_accessible_document(
    db: Session,
    document_id: str,
    customer_id: str
):

    document = db.scalar(
        select(KnowledgeDocument).where(
            KnowledgeDocument.id == document_id
        )
    )

    if document is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found."
        )

    if document.visibility == "PUBLIC":
        return document

    if (
        document.visibility == "PRIVATE"
        and document.owner_customer_id == customer_id
    ):
        return document

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found."
    )
