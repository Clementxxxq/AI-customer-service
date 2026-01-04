"""
Common utility functions
"""
from fastapi import HTTPException, status


def handle_not_found(resource_name: str):
    """Raise 404 Not Found exception"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource_name} not found"
    )


def handle_invalid_input(message: str):
    """Raise 400 Bad Request exception"""
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


def handle_conflict(message: str):
    """Raise 409 Conflict exception"""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )
