from django.contrib import admin
from django.urls import reverse
from django.utils import http, html
from django.utils.translation import gettext_lazy as _
from .models import Comment, Page


def url_filter_comments_by_page(page):
    return (
        reverse("admin:comments_comment_changelist")
        + "?"
        + http.urlencode({"page__id": f"{page.id}"})
    )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "comments_link")

    def comments_link(self, obj):
        url = url_filter_comments_by_page(obj)
        return html.format_html(
            '<a href="{}">{}</a>',
            url,
            _('%(count)d comments') % {
                'count': obj.comments.count()
            }
        )
    comments_link.short_description = _('Show comments')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("page_link", "author_link", "text", "date_created", "deleted")
    list_display_links = ("text", "date_created")

    def page_link(self, obj):
        page = obj.page
        url = url_filter_comments_by_page(page)
        return html.format_html('<a href="{}">{}</a>', url, str(page))
    page_link.short_description = _('Page')

    def author_link(self, obj):
        author = obj.author
        url = reverse("admin:auth_user_change", args=(author.id, ))
        return html.format_html('<a href="{}">{}</a>', url, str(author))
    author_link.short_description = _('Author')
