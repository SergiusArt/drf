from rest_framework import viewsets, generics, filters
from education import serializers
from education.models import Course, Lesson, Payment
from education.serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from users.models import ModeratorPermissions, IsOwner


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'delete']:
            self.permission_classes = [~ModeratorPermissions]
        return super(CourseViewSet, self).get_permissions()


# API для создания урока
class LessonCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~ModeratorPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# API для получения списка уроков
class LessonListAPIView(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]


# API для получения конкретного урока
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]


# API для обновления урока
class LessonUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [ModeratorPermissions | IsOwner]


# API для удаления урока
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [~ModeratorPermissions]


# API для получения списка платежей
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['payment_date']
    filterset_fields = ['course', 'lesson', 'payment_method']
    permission_classes = [ModeratorPermissions | IsOwner]


