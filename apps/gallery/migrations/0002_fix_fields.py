from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('gallery', '0001_initial'),
    ]
    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='file',
            field=models.FileField(upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/thumbs/'),
        ),
    ]
