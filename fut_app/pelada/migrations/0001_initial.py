# Generated by Django 5.2 on 2025-05-27 23:01

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
            name='Pelada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('hora', models.TimeField()),
                ('local', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('criador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peladas_criadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantePelada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ataque', models.IntegerField(default=0)),
                ('velocidade', models.IntegerField(default=0)),
                ('defesa', models.IntegerField(default=0)),
                ('passe', models.IntegerField(default=0)),
                ('controle', models.IntegerField(default=0)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pelada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participantes', to='pelada.pelada')),
            ],
            options={
                'unique_together': {('pelada', 'usuario')},
            },
        ),
    ]
