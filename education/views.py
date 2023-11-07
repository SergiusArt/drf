from rest_framework import viewsets, generics
from education import serializers
from education.models import Course, Lesson


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = Course.objects.all()


# API для создания урока
class LessonCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LessonSerializer


# API для получения списка уроков
class LessonListAPIView(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()


# API для получения конкретного урока
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()


# API для обновления урока
class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()


# API для удаления урока
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
