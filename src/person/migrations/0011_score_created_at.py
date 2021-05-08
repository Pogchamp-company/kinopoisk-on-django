# Generated by Django 3.1.5 on 2021-05-05 16:23

from django.db import migrations, models
import django.db.models.deletion
import django_minio_backend.models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_score_created_at'),
        ('person', '0010_role_name_longer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Персона', 'verbose_name_plural': 'Персоны'},
        ),
        migrations.AlterModelOptions(
            name='personrole',
            options={'verbose_name': 'Роль в фильме', 'verbose_name_plural': 'Роли в фильмах'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'Фото персоны', 'verbose_name_plural': 'Фотографии персон'},
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='person',
            name='death',
            field=models.DateField(null=True, verbose_name='Дата смерти'),
        ),
        migrations.AlterField(
            model_name='person',
            name='fullname',
            field=models.CharField(max_length=150, verbose_name='Полное имя'),
        ),
        migrations.AlterField(
            model_name='person',
            name='height',
            field=models.PositiveIntegerField(null=True, verbose_name='Рост в сантиметрах'),
        ),
        migrations.AlterField(
            model_name='person',
            name='ru_fullname',
            field=models.CharField(max_length=150, null=True, verbose_name='Полное имя (На русском)'),
        ),
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(choices=[('MALE', 'Мужчина'), ('FEMALE', 'Женщина')], max_length=6, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='movies.movie', verbose_name='Фильм'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='person.person', verbose_name='Персона'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='role_name',
            field=models.CharField(max_length=1000, null=True, verbose_name='Название роли'),
        ),
        migrations.AlterField(
            model_name='personrole',
            name='role_type',
            field=models.CharField(choices=[('DIRECTOR', 'Режиссер'), ('WRITER', 'Сценарист'), ('PRODUCER', 'Продюсер'), ('OPERATOR', 'Оператор'), ('COMPOSER', 'Композитор'), ('EDITOR', 'Монтажер'), ('ACTOR', 'Актер'), ('DESIGN', 'Постановщик'), ('VOICE_DIRECTOR', 'Звукорежиссер'), ('TRANSLATOR', 'Переводчик')], max_length=20, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='format',
            field=models.CharField(choices=[('LARGE', 'Большой'), ('MEDIUM', 'Средний'), ('SMALL', 'Маленький')], max_length=10, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(storage=django_minio_backend.models.MinioBackend(bucket_name='images'), upload_to=django_minio_backend.models.iso_date_prefix, verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='orientation',
            field=models.CharField(choices=[('VERTICAL', 'Вертикальный'), ('HORIZONTAL', 'Горизонтальный')], max_length=10, verbose_name='Ориентация'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='person.person', verbose_name='Персона'),
        ),
    ]