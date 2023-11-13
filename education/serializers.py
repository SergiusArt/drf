from rest_framework import serializers

from education.models import Course, Lesson, Payment


# Сериализатор уроков
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('course', 'title', 'description', 'preview', 'video_url')


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



