import re
from rest_framework import serializers

from education.models import Course, Lesson, Payment
from users.models import Subscription


# Сериализатор уроков
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'preview', 'video_url')

        def validate_description(self, value):
            # Проверяем, что описание не содержит ссылок на сторонние ресурсы кроме youtube.com
            pattern = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
            urls = re.findall(pattern, value)
            for url in urls:
                if 'youtube.com' not in url:
                    raise serializers.ValidationError("Ссылки на сторонние ресурсы не разрешены.")

            return value


# Сериализатор курсов
class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set', required=False)

    class Meta:
        model = Course
        fields = ('name', 'description', 'image', 'lesson_count', 'lessons')

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()


# Сериализатор платежей
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
