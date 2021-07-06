import graphene
from graphene import relay
import graphene_django

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

class Query(graphene.ObjectType):
    comment = relay.Node.Field(CommentGQLNode)

    comments = graphene_django.DjangoConnectionField(CommentGQLNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)


schema = graphene.Schema(query=Query)
