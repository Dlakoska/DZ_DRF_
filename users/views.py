from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.filters import PaymentFilter
from users.models import Payment, User
from users.permissions import IsOwner, IsUser
from users.serializers import PaymentSerializer, UserSerializer, UserNotOwnerSerializer


class PaymentViewSet(ModelViewSet):
    """Позволяет автоматически реализовать стандартные методы CRUD для модели Payment"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """ Этот метод срабатывает, когда пользователь создает новый курс через API."""

        payment = serializer.save()
        payment.owner = self.request.user
        payment.save()


class UserCreateAPIView(CreateAPIView):
    """Создать пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Список пользователей"""
    queryset = User.objects.all()
    serializer_class = UserNotOwnerSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Конкретный пользователь"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        # Если пользователь запрашивает свой профиль, используем полный сериализатор
        if self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserNotOwnerSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Удалить пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Изменить пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


