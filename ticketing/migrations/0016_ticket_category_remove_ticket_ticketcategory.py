# Generated by Django 5.2.4 on 2025-07-28 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0015_delete_helper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_category_name', models.CharField(max_length=255)),
                ('category_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='ticketCategory',
        ),
    ]
