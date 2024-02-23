"""
Model for advertisements
"""

from datetime import timezone

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.postgres.fields import ArrayField


class Advertisements(models.Model):
    """
    DB AD
    """

    CONDITION_CHOICES = [
        ("b/w", "Б/у"),
        ("new", "Новый"),
    ]
    CATEGORIES_CHOICES = [
        ("personal_effects", "Личные вещи"),
        ("electronics", "Электроника"),
        ("hobbies_and_recreation", "Хобби и отдых"),
        ("for_home_and_cottage", "Для дома и дачи"),
    ]
    SUBCATEGORIES_CHOICES = [
        ("clothes_shoes_accessories", "Одежда, обувь, аксессуары"),
        ("watches_and_jewelry", "Часы и украшения"),
        ("beauty_and_health", "Красота и здоровье"),
        ("household_appliances", "Бытовая техника"),
        ("furniture_and_interior", "Мебель и интерьер"),
        ("cookware_and_kitchenware", "Посуда и товары для кухни"),
        ("foodstuffs", "Продукты питания"),
        ("audio_and_video", "Аудио и видео"),
        ("games_consoles_programs", "Игры, приставки и программы"),
        ("PC", "ПК"),
        ("laptops", "Ноутбуки"),
        ("tablets_and_e-books", "Планшеты и электронные книги"),
        ("Phones", "Телефоны"),
        ("PC_Products", "Товары для ПК"),
        ("photographic_equipment", "Фототехника"),
        ("bicycles", "Велосипеды"),
        ("books_and_magazines", "Книги и журналы"),
        ("collecting", "Коллекционирование"),
        ("musical_instruments", "Музыкальные инструменты"),
        ("sports_and_recreation", "Спорт и отдых"),
    ]

    title = models.CharField(
        max_length=50,
        verbose_name="Title",
        null=False,
    )
    condition = models.CharField(
        null=False,
        choices=CONDITION_CHOICES,
        default="b/w",
    )
    description = models.TextField(
        max_length=1000,
        null=False,
        validators=[
            MinLengthValidator(
                limit_value=50,
                message="Minimum number of characters: 50",
            )
        ],
        verbose_name="description",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        verbose_name="Price",
    )
    owner = models.ForeignKey(
        "User.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="Owner",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data creation")
    location = models.TextField(
        max_length=1000,
        verbose_name="Location",
        default="",
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Category",
        choices=CATEGORIES_CHOICES,
        null=False,
    )
    subcategory = models.CharField(
        max_length=100,
        verbose_name="Subcategory",
        choices=SUBCATEGORIES_CHOICES,
        null=False,
    )
    images = ArrayField(
        models.URLField(
            max_length=500,
        ),
        blank=True,
        validators=[
            MinLengthValidator(
                limit_value=3,
                message="There must be at least three image",
            )
        ],
    )

    def __str__(self) -> str:
        return self.title
