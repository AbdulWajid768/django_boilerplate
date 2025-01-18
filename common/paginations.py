"""Pagination for Django App."""
from rest_framework.pagination import CursorPagination

DEFAULT_PAGE_SIZE = 10


class CustomCursorPagination(CursorPagination):
    """Custom class for cursor pagination to override settings."""

    page_size = DEFAULT_PAGE_SIZE
    ordering = '-created_at'
