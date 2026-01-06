# api/urls.py
from django.urls import path
from .views import (
    BusinessAPI,
    StatusAPI,
    CartAPI,
    UserOrderAPI,
    BusinessOrderAPI,
    ProductAPI,
    BusinessProductAPI,
    ProductByCategoryAPI,
    BusinessByCategoryAPI,
    GoogleAuthAPI,
    BusinessCategoryAPI,
    ProductCategoryAPI,
    UserTypeAPI,
    getBusiness
)

urlpatterns = [

    path("auth/google/", GoogleAuthAPI.as_view()),
    path("business/orders/", BusinessOrderAPI.as_view()),
    path("business/product/", BusinessProductAPI.as_view()),
    path("business/product/<slug:slug>/", BusinessProductAPI.as_view()),
    path("business/category/<int:category_id>/", BusinessByCategoryAPI.as_view()),

    path("business/", BusinessAPI.as_view()),
    path("business/profile/", getBusiness, name="getBusiness"),
    path("business/<slug:slug>/", BusinessAPI.as_view()),

    path("status/", StatusAPI.as_view()),
    path("status/<slug:slug>/", StatusAPI.as_view()),

    path("cart/", CartAPI.as_view()),
    path("cart/<int:item_id>/", CartAPI.as_view()),

    path("user/orders/", UserOrderAPI.as_view()),

    path("product/", ProductAPI.as_view()),
    path("product/<slug:slug>/", ProductAPI.as_view()),

    path("product/category/<int:category_id>/", ProductByCategoryAPI.as_view()),

    path("categories/business/", BusinessCategoryAPI.as_view()),
    path("categories/product/", ProductCategoryAPI.as_view()),
    path("user-types/", UserTypeAPI.as_view()),
]
