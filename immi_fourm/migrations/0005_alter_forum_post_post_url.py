# Generated by Django 3.2.5 on 2021-07-28 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immi_fourm', '0004_alter_forum_post_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum_post',
            name='post_url',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
