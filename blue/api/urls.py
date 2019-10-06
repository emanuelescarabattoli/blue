from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import GraphQLView

urlpatterns = [path("", csrf_exempt(GraphQLView.as_view(graphiql=True)))]
