import graphene
from graphene import relay
import graphene_django
from graphql_relay import from_global_id
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.translation import gettext_lazy as _

from commenti_server.utils import authenticated_users_only
import comments.settings
from comments.models import Comment
from comments.types import CommentNode

def get_comment_by_global_id(id, **kwargs):
    pk_type, pk = from_global_id(id)
    if not pk_type == 'CommentNode':
        raise ValidationError(
            _('Invalid type of ID: %(type)s'),
            code='invalid',
            params={'type': pk_type},
        )
    return Comment.objects.get(pk=pk, **kwargs)

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
            if comments.settings.COMMENTI_ALLOW_ANONYMOUS:
                author = None
            else:
                raise PermissionDenied(
                    _('You must be logged in')
                )

        if parent == None:
            parent_id = None
        else:
            # Parent comment must be on the same page
            # otherwise, Django raises a DoesNotExist exception
            parent_id = get_comment_by_global_id(parent, page_id=page).pk

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
    @authenticated_users_only
    def mutate_and_get_payload(cls, root, info, id):
        author = info.context.user
        comment = get_comment_by_global_id(id, author=author)
        comment.deleted = True
        comment.save()
        return DeleteComment(success=True)

class EditComment(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()
        text = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    @authenticated_users_only
    def mutate_and_get_payload(cls, root, info, id, text):
        author = info.context.user
        comment = get_comment_by_global_id(id, author=author)
        comment.text = text
        comment.save()
        return EditComment(success=True)

class CommentiSettings(graphene.ObjectType):
    allow_edit = graphene.Boolean()
    def resolve_allow_edit(root, info):
        return comments.settings.COMMENTI_ALLOW_EDIT

    allow_delete = graphene.Boolean()
    def resolve_allow_delete(root, info):
        return comments.settings.COMMENTI_ALLOW_DELETE

    allow_anonymous = graphene.Boolean()
    def resolve_allow_anonymous(root, info):
        return comments.settings.COMMENTI_ALLOW_ANONYMOUS

class Mutation(graphene.ObjectType):
    write_comment = WriteComment.Field()
    if comments.settings.COMMENTI_ALLOW_EDIT:
        edit_comment = EditComment.Field()
    if comments.settings.COMMENTI_ALLOW_DELETE:
        delete_comment = DeleteComment.Field()

class Query(graphene.ObjectType):
    comment = relay.Node.Field(CommentNode)

    comments = graphene_django.DjangoConnectionField(CommentNode, page=graphene.String())
    def resolve_comments(root, info, page, **args):
        return Comment.objects.filter(page=page, parent=None)

    settings = graphene.Field(CommentiSettings)
    def resolve_settings(root, info):
        return {}
