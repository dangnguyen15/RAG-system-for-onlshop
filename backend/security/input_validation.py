
import re
import unicodedata

from fastapi import HTTPException, status


# =========================================================
# CONFIGURATION
# =========================================================

MAX_MESSAGE_LENGTH = 2000
MIN_MESSAGE_LENGTH = 1


# =========================================================
# NORMALIZE MESSAGE
# =========================================================

def normalize_message(message: str) -> str:

    if not isinstance(message, str):

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message must be a string."
        )

    # Normalize Unicode
    message = unicodedata.normalize(
        "NFC",
        message
    )

    # Remove leading/trailing whitespace
    message = message.strip()

    # Replace multiple spaces/newlines
    message = re.sub(
        r"\s+",
        " ",
        message
    )

    return message


# =========================================================
# VALIDATE MESSAGE
# =========================================================

def validate_chat_message(message: str) -> str:

    message = normalize_message(message)

    if len(message) < MIN_MESSAGE_LENGTH:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty."
        )

    if len(message) > MAX_MESSAGE_LENGTH:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Message exceeds maximum length of "
                + str(MAX_MESSAGE_LENGTH)
                + " characters."
            )
        )

    return message


# =========================================================
# VALIDATE SESSION TITLE
# =========================================================

def validate_session_title(title: str) -> str:

    title = normalize_message(title)

    if len(title) > 200:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Session title is too long."
        )

    return title
