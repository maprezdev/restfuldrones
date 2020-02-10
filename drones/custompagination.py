# drones/custompagination.py file
from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    """overrides the value of maximum_limit to 8"""
    max_limit = 8
