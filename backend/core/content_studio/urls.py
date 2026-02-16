from django.urls import path
from . import views

urlpatterns = [
    path("briefs/create", views.create_brief, name="create_brief"),
    path("briefs/<uuid:workspace_id>", views.list_briefs, name="list_briefs"),
    path("briefs/<uuid:brief_id>/variants", views.get_brief_variants, name="get_brief_variants"),
    path("variants/<uuid:variant_id>/approve", views.approve_variant, name="approve_variant"),
]
