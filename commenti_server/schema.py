import graphene
import graphene_django
import graphql_jwt
from graphql_jwt.shortcuts import create_refresh_token, get_token
from django.contrib import auth

import comments.schema

class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = auth.get_user_model()
        fields = (
            'id',
            'username'
        )

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class CreateUser(graphene.Mutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, username, password, email):
        user_model = auth.get_user_model()
        user = user_model.objects.create_user(
            username, email, password
        )

        return CreateUser(
            user=user,
            token=get_token(user),
            refresh_token=create_refresh_token(user)
        )

class Query(comments.schema.Query, graphene.ObjectType):
    current_user = graphene.Field(UserType)
    def resolve_current_user(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user

class Mutation(comments.schema.Mutation, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
