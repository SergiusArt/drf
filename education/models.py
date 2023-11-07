from django.db import models
from src.constants import NULLABLE


# Класс модели "Курс": название, превью (картинка), описание
class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(upload_to='courses', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    # дата и время создания курса
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return self.name


# Класс модели "Урок": курс, название, описание, превью (картинка), ссылка на видео
class Lesson(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='курс')
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    preview = models.ImageField(upload_to='lesson', **NULLABLE, verbose_name='первью')
    video_url = models.URLField(**NULLABLE, verbose_name='видео')
    # дата и время создания урока
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return self.title
