from django.urls import path

from biocrust_app.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    ActivateUser,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path('activate/<uid>/<token>', view=ActivateUser.as_view({'get': 'activation'}), name='activation'),
]
