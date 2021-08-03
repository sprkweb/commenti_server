import graphene
from graphene import relay
import graphene_django
from graphql_relay import from_global_id
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _

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

class WriteComment(relay.ClientIDMutation):
    class Input:
        text = graphene.String(required=True)
        page = graphene.String(required=True)
        parent = graphene.ID()

    comment = graphene.Field(CommentNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, text, page, parent = None):
        author = info.context.user
        if not author.is_authenticated:
            # TODO: anonymous comments support
            raise PermissionDenied(
                _('You must be logged in to write a comment')
            )

        if parent == None:
            parent_id = None
        else:
            parent_type, parent_id = from_global_id(parent)
            if not parent_type == 'CommentNode':
                raise ValidationError(
                    _('Invalid type of parent ID: %(type)s'),
                    code='invalid',
                    params={'type': parent_type},
                )
            # Parent comment must be on the same page
            # otherwise, Django raises a DoesNotExist exception
            Comment.objects.get(pk=parent_id, page_id=page)

        new_comment = Comment(
            text=text,
            page_id=page,
            parent_id=parent_id,
            author=author)
        new_comment.save()
        return WriteComment(comment=new_comment)

class Mutation(graphene.ObjectType):
    write_comment = WriteComment.Field()

class Query(graphene.ObjectType):
    comment = relay.Node.Field(CommentNode)

    comments = graphene_django.DjangoConnectionField(CommentNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)
