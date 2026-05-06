from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_readd_service_facility_team'),
    ]

    operations = [
        migrations.RenameModel('Facility', 'Amenity'),
        migrations.RenameModel('FacilityImage', 'AmenityImage'),
        migrations.AlterModelOptions(
            name='amenity',
            options={'ordering': ['order'], 'verbose_name_plural': 'Amenities'},
        ),
    ]