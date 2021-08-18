import graphene
from graphene import relay
import graphene_django
from graphql_relay import from_global_id
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.translation import gettext_lazy as _

import comments.settings
from comments.models import Comment
from comments.types import CommentNode

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

class DeleteComment(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        author = info.context.user
        if not author.is_authenticated:
            # TODO: anonymous comments support
            raise PermissionDenied(
                _('You must be logged in to delete a comment')
            )

        pk_type, pk = from_global_id(id)
        if not pk_type == 'CommentNode':
            raise ValidationError(
                _('Invalid type of ID: %(type)s'),
                code='invalid',
                params={'type': pk_type},
            )

        comment = Comment.objects.get(pk=pk, author=author)
        comment.deleted = True
        comment.save()

        return DeleteComment(success=True)

class Mutation(graphene.ObjectType):
    write_comment = WriteComment.Field()
    # if comments.settings.COMMENTI_ALLOW_EDIT:
    #   edit_comment = EditComment.Field()
    if comments.settings.COMMENTI_ALLOW_DELETE:
        delete_comment = DeleteComment.Field()

class Query(graphene.ObjectType):
    comment = relay.Node.Field(CommentNode)

    comments = graphene_django.DjangoConnectionField(CommentNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)
