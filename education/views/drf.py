from rest_framework import viewsets, generics, filters
from education import serializers
from education.models import Course, Lesson, Payment
from education.serializers import PaymentSerializer, SubscriptionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from users.models import ModeratorPermissions, IsOwner, Subscription


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CourseSerializer
    permission_classes = [ModeratorPermissions | IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [~ModeratorPermissions]
        # Редактировать и просматривать могут только модераторы и владельцы
        if self.action in ['update', 'retrieve']:
            self.permission_classes = [ModeratorPermissions | IsOwner]
        return super(CourseViewSet, self).get_permissions()

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(owner=user).order_by('id')


# API для создания урока
class LessonCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.order_by('id')
    permission_classes = [~ModeratorPermissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# API для получения списка уроков
class LessonListAPIView(generics.ListAPIView):
    serializer_class = serializers.LessonSerializer
    queryset = Lesson.objects.order_by('id')
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
    permission_classes = [~ModeratorPermissions | IsOwner]


# API для получения списка платежей
class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['payment_date']
    filterset_fields = ['course', 'lesson', 'payment_method']
    permission_classes = [ModeratorPermissions | IsOwner]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


