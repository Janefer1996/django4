from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseForPublication(models.Model):
    """Базовые пфраметры классов"""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True,
                                      blank=False)

    class Meta:
        """Абстрактность модели"""

        abstract = True


class Category(BaseForPublication):
    """Категория поста"""

    title = models.CharField(
        'Заголовок',
        max_length=256,
        blank=False
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        blank=False,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(BaseForPublication):
    """Место расположения"""

    name = models.CharField('Название места', max_length=256, blank=False)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(BaseForPublication):
    """Посты"""

    title = models.CharField('Название', max_length=256, blank=False)
    text = models.TextField('Текст', blank=False)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='publications',
        blank=False
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        related_name='publications',
        null=True,
        blank=False
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='publications',
        null=True,
        blank=False
    )
    image = models.ImageField(
        upload_to="images",
        blank=True,
        verbose_name="Изображение",)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Комментарий"""

    text = models.TextField(
        verbose_name="Комментарий",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = "comments"
        ordering = ("created_at",)

    def __str__(self):
        return f"Комментарий пользователя {self.author}"