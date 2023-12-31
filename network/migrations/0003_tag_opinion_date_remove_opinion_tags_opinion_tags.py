# Generated by Django 4.2.1 on 2023-09-08 11:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_opinion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='opinion',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 17, 10, 0, 751428)),
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='tags',
        ),
        migrations.AddField(
            model_name='opinion',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='opinion_tags', to='network.tag'),
        ),
    ]
