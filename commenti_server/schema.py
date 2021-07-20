import graphene
from graphene import relay
import graphene_django
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import auth
from django.contrib.auth.models import User
from comments.models import Comment

class UserGQLType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name'
        )

class CommentGQLNode(graphene_django.DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'text',
            'author',
            'date_created',
            'date_edited',
            'parent',
            'children'
        )
        interfaces = (relay.Node, )

class GQLLogin(graphene.Mutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserGQLType)

    @classmethod
    def mutate(cls, root, info, username, password):
        user = auth.authenticate(
            info.context,
            username=username,
            password=password
        )
        if user is not None:
            auth.login(info.context, user)
            return GQLLogin(user=user)
        else:
            raise ValidationError(
                _('Incorrect username or password'),
                code='invalid login'
            )

class GQLLogout(graphene.Mutation):
    class Input:
        pass

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info):
        auth.logout(info.context)
        return GQLLogout(ok=True)

class Query(graphene.ObjectType):
    comment = relay.Node.Field(CommentGQLNode)

    comments = graphene_django.DjangoConnectionField(CommentGQLNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)

class Mutation(graphene.ObjectType):
    login = GQLLogin.Field()
    logout = GQLLogout.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
