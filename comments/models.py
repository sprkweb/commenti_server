from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Page(models.Model):
    id = models.CharField(
        _('Unique ID'),
        max_length=32,
        primary_key=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class Comment(models.Model):
    text = models.TextField(_('Text'))

    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        related_name='comments',
        null=True)

    date_created = models.DateTimeField(
        _('Created'),
        auto_now_add=True,
        editable=False
    )
    date_edited = models.DateTimeField(
        _('Last edited'),
        auto_now=True,
        editable=False
    )

    page = models.ForeignKey(
        Page,
        verbose_name=_('Page'),
        on_delete=models.CASCADE,
        related_name='comments'
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent comment'),
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )

    deleted = models.BooleanField(
        verbose_name=_('Deleted'),
        default=False)

    def __str__(self) -> str:
        return _('From %(user)s, %(date)s') % {
            'user': self.author,
            'date': self.date_created
        }

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
