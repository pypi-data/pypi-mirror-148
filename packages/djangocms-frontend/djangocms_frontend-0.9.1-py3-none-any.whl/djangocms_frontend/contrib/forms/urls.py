from django.urls import include, path

from . import views

app_name = "djangocms_frontend"

urlpatterns = [
    path("f<form_id>", views.AjaxView.as_view(), name="ajaxform"),
    path(
        "<int:instance_id>/<path:parameter>",
        views.AjaxView.as_view(),
        name="ajaxview",
    ),
    path(
        "<int:instance_id>",
        views.AjaxView.as_view(),
        name="ajaxview",
    ),
]


urls = include("djangocms_frontend.contrib.forms.urls", namespace="dcf_forms")
