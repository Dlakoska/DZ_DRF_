from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import PaymentViewSet, UserRetrieveAPIView, UserCreateAPIView, UserListAPIView
from django.urls import path


app_name = UsersConfig.name
router = SimpleRouter()
router.register("payments", PaymentViewSet)
urlpatterns = [
    path("users/", UserListAPIView.as_view(), name="users"),
    path("user/create/", UserCreateAPIView.as_view(), name="user_create"),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user_retrieve"),

]
urlpatterns += router.urls