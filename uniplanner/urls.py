from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logoff", views.logoff, name="logoff"),
    path('add_event', views.add_event, name="add_event"),
    path('update', views.update, name="update"),
    path('delete',views.delete, name='delete'),
    path('addmodule', views.addmodule, name='addmodule'),
    path('deletemod', views.deletemod, name='deletemod'),
    path('module/<int:id>', views.moduled, name='module'),
    path('done', views.done, name='done'),
    path('add_task/<int:module_id>', views.add_task, name='add_task'),
    path('asked', views.asked, name='asked'),
    path('add_question/<int:module_id>', views.add_question, name='add_question'),
    path('filter', views.filter, name='filter')
]