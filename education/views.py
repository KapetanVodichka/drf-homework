import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from config import settings
from education.models import Course, Lesson, Payment, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import IsMember, IsModerator, IsOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from users.models import UserRole


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsMember]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated, IsOwner]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.Moderator:
            return Course.objects.all()
        else:
            return Course.objects.filter(user=user)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.user = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        updated_course = serializer.save()
        check_update.delay(
            updated_course.pk,
            updated_course.title,
            updated_course.user.email,
            updated_course.user.pk
        )


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.user = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.Moderator:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(user=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('-date')

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.Moderator:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(user=user)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        new_pay = serializer.save()

        stripe.api_key = settings.PAY_API_KEY
        stripe_pay = stripe.PaymentIntent.create(
            amount=serializer.validated_data['course'].amount,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )

        new_pay.user = self.request.user
        new_pay.price = serializer.validated_data['course'].amount
        new_pay.stripe_id = stripe_pay["id"]
        new_pay.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]