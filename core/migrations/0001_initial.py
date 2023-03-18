# Generated by Django 4.1.5 on 2023-03-18 12:48

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('venue', models.CharField(max_length=1000, null=True)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('Entertainment', 'ENtertainment'), ('Tech', 'TEch'), ('Professional', 'PRofessional'), ('Religious', 'REligious')], max_length=50, null=True)),
                ('poster', models.ImageField(null=True, upload_to='media')),
                ('ticket_price', models.FloatField(null=True)),
                ('tickets_ava', models.IntegerField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=500, unique=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='IpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tix_code', models.CharField(max_length=500, null=True, unique=True)),
                ('tix_mail', models.CharField(max_length=500, null=True)),
                ('tix_name', models.CharField(max_length=500, null=True)),
                ('tix_phone', models.CharField(max_length=500, null=True)),
                ('ticket_price', models.FloatField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('comment', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
            ],
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('biz_name', models.CharField(max_length=1000, null=True)),
                ('slug', models.SlugField(max_length=500, unique=True)),
                ('account_number', models.IntegerField(null=True)),
                ('bank_code', models.CharField(choices=[('044', 'Access Bank'), ('023', 'Citibank'), ('050', 'Ecobank'), ('214', 'FCMB'), ('070', 'Fidelity'), ('011', 'First Bank'), ('058', 'GTB'), ('030', 'Heritage'), ('301', 'Jaiz Bank'), ('082', 'Keystone'), ('526', 'Parallex'), ('101', 'Providus'), ('221', 'Stanbic'), ('076', 'Skye Bank'), ('068', 'Standard Bank'), ('232', 'Sterling Bank'), ('100', 'Suntrust Bank'), ('102', 'Titan Trust'), ('032', 'Union Bank'), ('033', 'United Bank'), ('215', 'Unity Bank'), ('035', 'Wema Bank'), ('057', 'Zenith Bank')], max_length=4, null=True)),
                ('account_name', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', models.ImageField(null=True, upload_to='media')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.organizer'),
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]