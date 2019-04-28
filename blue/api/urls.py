from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import PrivateGrapQLView

urlpatterns = [
    path("", csrf_exempt(PrivateGrapQLView.as_view(graphiql=True)))
]
