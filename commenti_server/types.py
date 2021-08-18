import graphene_django
from django.contrib import auth

class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = auth.get_user_model()
        fields = (
            'id',
            'username'
        )
