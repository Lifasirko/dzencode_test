# Generated by Django 5.1.3 on 2024-11-26 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text_file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.CharField(max_length=255),
        ),
    ]
