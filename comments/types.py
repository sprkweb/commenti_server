import graphene
from graphene import relay
import graphene_django

from .models import Comment
from commenti_server.types import UserType

def resolve_if_shown(comment, value):
    if not comment.deleted:
        return value
    else:
        return None

class CommentNode(graphene_django.DjangoObjectType):
    class Meta:
        model = Comment
        # when you want to add some fields here,
        # note: all fields here remain visible even after the
        # comment is deleted
        fields = (
            'date_created',
            'date_edited',
            'parent',
            'children',
            'deleted'
        )
        interfaces = (relay.Node, )

    author = graphene.Field(UserType)
    def resolve_author(parent, info):
        return resolve_if_shown(parent, parent.author)

    text = graphene.String()
    def resolve_text(parent, info):
        return resolve_if_shown(parent, parent.text)
