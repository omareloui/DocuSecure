# Generated by Django 5.1.7 on 2025-03-28 02:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('filename', models.CharField(max_length=64)),
                ('path', models.CharField(max_length=64)),
                ('url', models.CharField(max_length=64)),
                ('size', models.IntegerField()),
                ('mimetype', models.CharField(max_length=64)),
                ('classification', models.CharField(max_length=64, null=True)),
                ('confidence', models.FloatField(default=0)),
                ('keywords', models.TextField(null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Parsing'), ('PARSED', 'Parsed')], default='PENDING', max_length=16)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
