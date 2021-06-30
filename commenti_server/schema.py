import graphene
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

class CommentGQLType(graphene_django.DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'date_created',
            'date_edited'
        )

class Query(graphene.ObjectType):
    # TODO: temporary query
    all_comments = graphene.List(CommentGQLType)
    def resolve_all_comments(root, info):
        return Comment.objects.all()

schema = graphene.Schema(query=Query)
