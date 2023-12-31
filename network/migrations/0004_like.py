# Generated by Django 4.2.2 on 2023-06-23 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likers', to='network.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liking', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
