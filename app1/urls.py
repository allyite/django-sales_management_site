from django.urls import path

from . import views

app_name= "app1"
urlpatterns = [
    path('minv', views.mng_inv, name='manage_inv'),
    path('tinv', views.trck_inv, name='track_inv'),
    path('orders', views.s_orders, name='sales_orders'),
    path('orders/<str:oaction>/<int:oid>', views.mng_order, name='mng_order'),
    path('prod/<int:prodid>', views.prod, name='product'),
]
