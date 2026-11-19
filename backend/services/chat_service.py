
from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from backend.database.models import (
    ChatSession,
    ChatMessage
)

from backend.security.input_validation import (
    validate_chat_message,
    validate_session_title
)

from backend.security.authorization import (
    get_owned_chat_session
)


# =========================================================
# CREATE CHAT SESSION
# =========================================================

def create_chat_session(
    db: Session,
    customer_id: str,
    session_title: str = None
):

    if session_title:

        session_title = validate_session_title(
            session_title
        )

    chat_session = ChatSession(
        customer_id=customer_id,
        session_title=session_title or "New conversation",
        is_active=True
    )

    try:

        db.add(chat_session)

        db.commit()

        db.refresh(chat_session)

        return chat_session

    except Exception:

        db.rollback()

        raise


# =========================================================
# GET CUSTOMER CHAT SESSION
# =========================================================

def get_chat_session(
    db: Session,
    session_id: str,
    customer_id: str
):

    return get_owned_chat_session(
        db=db,
        session_id=session_id,
        customer_id=customer_id
    )


# =========================================================
# GENERATE TEMPORARY ASSISTANT RESPONSE
# =========================================================

def generate_test_response(message: str) -> str:
    """
    Temporary response for Stage 2.

    This function will be replaced by the AI pipeline
    in later stages.
    """

    return (
        "Xin chào! Tôi đã nhận được câu hỏi của bạn: "
        + message
        + ". Hệ thống AI đang trong giai đoạn xây dựng "
        "và sẽ sớm hỗ trợ bạn tốt hơn."
    )


# =========================================================
# PROCESS CHAT MESSAGE
# =========================================================

def process_chat_message(
    db: Session,
    session_id: str,
    customer_id: str,
    message: str
):

    # 1. Validate message
    message = validate_chat_message(message)

    # 2. Verify session ownership
    chat_session = get_owned_chat_session(
        db=db,
        session_id=session_id,
        customer_id=customer_id
    )

    if not chat_session.is_active:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat session is inactive."
        )

    try:

        # 3. Save user message
        user_message = ChatMessage(
            session_id=chat_session.id,
            sender="USER",
            content=message
        )

        db.add(user_message)

        db.flush()

        # 4. Generate temporary response
        assistant_content = generate_test_response(
            message
        )

        # 5. Save assistant response
        assistant_message = ChatMessage(
            session_id=chat_session.id,
            sender="ASSISTANT",
            content=assistant_content
        )

        db.add(assistant_message)

        # 6. Update session title if it is new
        if (
            chat_session.session_title == "New conversation"
            or not chat_session.session_title
        ):

            chat_session.session_title = message[:50]

        # 7. Commit transaction
        db.commit()

        db.refresh(user_message)
        db.refresh(assistant_message)
        db.refresh(chat_session)

        return {
            "session_id": chat_session.id,
            "user_message": user_message,
            "assistant_message": assistant_message
        }

    except Exception:

        db.rollback()

        raise
