import stripe
from rest_framework import serializers

from config import settings
from education.models import Lesson, Course, Payment, Subscription
from education.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            LinkValidator(field='link_video')
        ]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_lesson_count(self, instance):
        return instance.lesson_set.count()

    def get_subscription_status(self, instance):
        if hasattr(instance, 'subscription'):
            return instance.subscription.status
        return False


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        if not data.get('course'):
            raise serializers.ValidationError("Выберите курс.")
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('course', 'status')


class PaymentStripeSerializer(PaymentSerializer):
    stripe = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_stripe(self, instance):
        stripe.api_key = settings.PAY_API_KEY
        stripe_data = stripe.PaymentIntent.retrieve(
            instance.stripe_id,
        )
        return stripe_data