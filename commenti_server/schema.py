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
    comments = graphene.List(CommentGQLType, page=graphene.String())
    def resolve_comments(root, info, page):
        return Comment.objects.filter(page=page)

schema = graphene.Schema(query=Query)
