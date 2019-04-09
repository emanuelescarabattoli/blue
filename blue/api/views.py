from django.contrib.auth.mixins import UserPassesTestMixin
from graphene_django.views import GraphQLView


class PrivateGrapQLView(UserPassesTestMixin, GraphQLView):
    """
    a view accessible only for authenticated users
    """

    def test_func(self):
        """
        test if user is loggen in
        """

        return self.request.user.is_authenticated
