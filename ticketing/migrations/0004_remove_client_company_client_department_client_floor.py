# Generated by Django 5.2.3 on 2025-07-22 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_alter_ticket_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='company',
        ),
        migrations.AddField(
            model_name='client',
            name='department',
            field=models.IntegerField(choices=[(7, 'No Department Selected'), (0, 'Human Resource Administration'), (1, 'Planning and Information'), (2, 'Local Government Administation'), (3, 'Rural Development'), (4, 'Office of the Minister'), (5, 'Procurement Department'), (6, 'Finance Department')], default=7),
        ),
        migrations.AddField(
            model_name='client',
            name='floor',
            field=models.IntegerField(choices=[(6, 'Floor Not Selected'), (0, 'Ground Floor'), (1, '1st Floor'), (2, '2nd Floor'), (3, 'Third Floor'), (4, 'Fourth Floor'), (5, 'Fifth Floor')], default=6),
        ),
    ]
