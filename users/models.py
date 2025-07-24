from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User, где для аутентификации
    используется номер телефона вместо username.
    """
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным номером телефона и паролем.
        """
        if not phone_number:
            raise ValueError(_('The Phone Number must be set'))
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    # Убираем стандартное поле username, оно нам не нужно.
    username = None

    # Номер телефона становится главным полем для аутентификации.
    # Оно должно быть уникальным.
    phone_number = models.CharField(
        _('номер телефона'),
        max_length=15,
        unique=True,
        help_text=_('Обязательное поле. 15 символов или меньше.')
    )

    # 6-значный инвайт-код, который принадлежит этому пользователю.
    # Он может быть пустым, так как генерируется после создания пользователя.
    invite_code = models.CharField(
        _('личный инвайт-код'),
        max_length=6,
        unique=True,
        blank=True,
        null=True
    )

    activated_invite_from = models.ForeignKey(
        'self',
        verbose_name=_('активированный инвайт-код от'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referred_users'
    )

    # Указываем, какое поле будет использоваться для логина.
    USERNAME_FIELD = 'phone_number'
    
    # Список имен полей, которые будут запрашиваться при создании
    # пользователя через команду createsuperuser.
    REQUIRED_FIELDS = []

    # Подключаем наш кастомный менеджер.
    objects = UserManager()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.phone_number