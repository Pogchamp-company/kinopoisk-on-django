# Generated by Django 3.1.5 on 2021-08-30 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_Score_created_at_to_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='kp_id',
            field=models.PositiveIntegerField(default=1, unique=False),
        ),
        migrations.RunSQL('''UPDATE movies_movie SET kp_id = id '''),
        migrations.AlterField(
            model_name='movie',
            name='kp_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
