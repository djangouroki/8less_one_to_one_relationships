from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

# from django.contrib.auth.models import User as UserModel
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Employee(models.Model):
    """Сотрудник"""

    class SexChoices(models.TextChoices):
        MALE = 'm', 'Мужской'
        FEMALE = 'f', 'Женский'

    entry_date = models.DateField(auto_now_add=True)
    sex = models.CharField(
        choices=SexChoices.choices,
        max_length=1,
    )

    user = models.OneToOneField(
        # User,
        # UserModel,
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    def __str__(self):
        return f'{self.user}: {self.get_sex_display()} ({self.entry_date})'


class Place(models.Model):
    """Место расположения"""

    address = models.CharField(max_length=200)

    def __str__(self):
        return f"Адрес: {self.address}"


class Cafeteria(models.Model):
    """Кафетерий"""

    name = models.CharField(max_length=50)

    administrator = models.OneToOneField(
        "o2o.Employee",
        on_delete=models.PROTECT,
        related_name='acafeteria',
    )
    cleaner = models.OneToOneField(
        "o2o.Employee",
        on_delete=models.PROTECT,
        related_name='ccafeteria',
    )
    place = models.OneToOneField(
        "o2o.Place",
        on_delete=models.PROTECT,
        primary_key=True,
    )

    class Meta:
        verbose_name = _("cafeteria")
        verbose_name_plural = _("cafeterias")

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        if hasattr(self, 'administrator') \
            and hasattr(self.administrator, 'ccafeteria') \
                and self.administrator.ccafeteria.pk != self.pk:
            errors.update({
                'administrator': (
                    f'{self.administrator} уже работает '
                    f'клинером в {self.administrator.ccafeteria}'
                )
            })
        if hasattr(self, 'cleaner') \
            and hasattr(self.cleaner, 'acafeteria') \
                and self.cleaner.acafeteria.pk != self.pk:
            errors.update({
                'cleaner': (
                    f'{self.cleaner} уже работает '
                    f'администратором в {self.cleaner.acafeteria}'
                )
            })
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
