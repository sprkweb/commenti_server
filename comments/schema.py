import graphene
from graphene import relay
import graphene_django

from comments.models import Comment

class CommentNode(graphene_django.DjangoObjectType):
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
    comment = relay.Node.Field(CommentNode)

    comments = graphene_django.DjangoConnectionField(CommentNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)
