"""RBAC (Role-Based Access Control) — FastAPI dependencies for role enforcement.

Usage:
    from backend.auth.rbac import require_role, require_admin

    @router.get("/admin/users")
    def list_users(user=Depends(require_admin)):
        ...

    @router.get("/instructor/students")
    def list_students(user=Depends(require_instructor_or_admin)):
        ...
"""
from functools import wraps
from fastapi import Depends, HTTPException, status
from ..models import User
from .router import require_user


def require_role(*allowed_roles: str):
    """Create a dependency that requires the user to have one of the allowed roles.

    Args:
        *allowed_roles: Role names that are permitted (e.g., "admin", "instructor")

    Returns:
        A FastAPI dependency function

    Example:
        @router.get("/admin-only")
        def admin_endpoint(user=Depends(require_role("admin"))):
            ...
    """
    async def role_checker(user: User = Depends(require_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role: {', '.join(allowed_roles)}"
            )
        return user
    return role_checker


# Pre-built role dependencies for convenience
require_admin = require_role("admin")
require_instructor_or_admin = require_role("instructor", "admin")
require_student_or_above = require_role("student", "instructor", "admin")
