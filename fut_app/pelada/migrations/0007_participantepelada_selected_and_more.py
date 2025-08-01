# Generated by Django 4.2.11 on 2025-06-09 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pelada', '0006_alter_participantepelada_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='participantepelada',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participantepelada',
            name='ataque',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='participantepelada',
            name='controle',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='participantepelada',
            name='defesa',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='participantepelada',
            name='passe',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='participantepelada',
            name='velocidade',
            field=models.IntegerField(default=5),
        ),
    ]
