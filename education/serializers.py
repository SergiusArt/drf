import re
from rest_framework import serializers
import stripe
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

    def to_representation(self, instance):
        # Получаем представление экземпляра с помощью родительского метода
        representation = super().to_representation(instance)

        # Устанавливаем ключ API для stripe
        stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

        # Создаем цену для продукта с помощью stripe
        response_price = stripe.Price.create(
            unit_amount=22222,
            currency="usd",
            recurring={"interval": "year"},
            product="prod_P13LoGhQ2EHrYU",
        )

        # Получаем ID цены
        price_id = response_price['id']

        # Создаем сессию оплаты с помощью stripe
        response_session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": price_id,
                    "quantity": 2,
                },
            ],
            mode="subscription",
        )

        # Получаем URL для оплаты
        pay_url = response_session['url']

        # Добавляем ссылку на оплату в представление
        representation['payment_link'] = pay_url

        # Возвращаем представление
        return representation


# Сериализатор платежей
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('user', 'payment_date', 'course', 'lesson', 'amount', 'payment_method')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
