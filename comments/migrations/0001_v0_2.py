# Generated by Django 3.2.5 on 2021-08-25 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Unique ID')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('date_edited', models.DateTimeField(auto_now=True, verbose_name='Last edited')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='comments.page', verbose_name='Page')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='comments.comment', verbose_name='Parent comment')),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
