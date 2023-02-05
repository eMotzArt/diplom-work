# Generated by Django 4.1.5 on 2023-02-01 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_alter_category_board'),
        ('bot', '0005_rename_user_tguser_app_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TgState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.PositiveSmallIntegerField(choices=[(1, 'Выбор не выполнен'), (2, 'Категория выбрана'), (3, 'Заголовок выбран')], default=1)),
                ('title', models.CharField(max_length=100)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='goals.category')),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.tguser')),
            ],
        ),
    ]
