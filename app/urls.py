
from django.urls import path, include
from . import views


app_name = 'jogo'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('jogos/', views.Games.as_view(), name='games'),
    path('shop/<int:id>', views.Shop.as_view(), name='shop'),
    path('shop', views.ShopPage.as_view(), name='shopping')
    # path('carrinho<int:id>', views.Shop.as_view(), name='shop')
]


