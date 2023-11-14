from rest_framework.pagination import PageNumberPagination


class CoursePaginator(PageNumberPagination):
    page_size = 12


class LessonPaginator(PageNumberPagination):
    page_size = 12
