from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    # path('', views.index, name='main'),
    path("main/", views.index_no_gc, name="main_no_gc"),
    path("getcourse/", views.index_gc, name="main_gc"),
    # path('order/', views.pay_with_robokassa),
    path("order_from_gc/", views.order_from_gc),
    path("profile/", views.profile, name="profile"),
    path("profile/my_test_results/", views.profile_test_results, name="profile_test_results",),
    path("profile/my_group/", views.profile_my_group, name="profile_my_group"),
    path("profile/my_group/choose/", views.profile_my_group_choose, name="profile_my_group_choose",),
    path("profile/logout/", views.profile_logout, name="profile_logout"),
    path("update_session/", views.update_session),
    path("test/<str:test_name>/", views.test, name="test"),
    # path('register_answer/', views.register_answer),
    # path('get_answer/', views.get_answer),
    path("get_result/", views.get_result, name="result"),
    # path('my_order/', views.my_order, name='my_order'),
    path("create_order_from_gc/", views.create_order_from_gc, name="create_order_from_gc"),
    path("register_answer/", views.register_answer_view, name="register_answer"),
    path("get_answers/", views.get_answers_view, name="get_answers"),
    path("register_results/", views.register_results_view, name="register_results"),
]
