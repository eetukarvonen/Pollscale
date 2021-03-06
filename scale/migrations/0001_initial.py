# Generated by Django 3.1.7 on 2021-03-11 09:05

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
            name='Scale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale_title', models.CharField(max_length=200)),
                ('yay_or_nay_of_parent', models.CharField(blank=True, max_length=4, null=True)),
                ('nays', models.IntegerField(default=0)),
                ('yays', models.IntegerField(default=0)),
                ('parent_scale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scale.scale')),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(blank=True, max_length=8, null=True)),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scale.scale')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
