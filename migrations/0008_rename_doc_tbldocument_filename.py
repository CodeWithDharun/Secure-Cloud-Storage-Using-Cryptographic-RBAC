# Generated by Django 3.2.12 on 2022-04-25 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ERP', '0007_rename_document_tbldocument_doc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbldocument',
            old_name='doc',
            new_name='filename',
        ),
    ]
