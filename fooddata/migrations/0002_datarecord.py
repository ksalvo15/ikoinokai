# Generated by Django 2.2.5 on 2024-08-29 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fooddata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('data', models.IntegerField()),
                ('other_stuff', models.CharField(max_length=255)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fooddata.Document')),
            ],
        ),
    ]
