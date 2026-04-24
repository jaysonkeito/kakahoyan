from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/'),
        ),
    ]
