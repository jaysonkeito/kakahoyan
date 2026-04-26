from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero_description',
            field=models.TextField(blank=True, default='Kakahoyan offers an exclusive venue for weddings, celebrations, and gatherings — featuring a fully air-conditioned Glass Pavilion for up to 250 guests and a stunning outdoor platform.'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hours',
            field=models.CharField(blank=True, default='Always open for inquiries', max_length=100),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('icon', models.CharField(choices=[('bi-hearts', 'Hearts (Weddings)'), ('bi-balloon', 'Balloon (Birthdays)'), ('bi-people', 'People (Reunions)'), ('bi-mortarboard', 'Mortarboard (Graduation)'), ('bi-briefcase', 'Briefcase (Company Events)'), ('bi-stars', 'Stars (Socials)'), ('bi-music-note', 'Music Note'), ('bi-camera', 'Camera'), ('bi-cup-hot', 'Cup (Catering)'), ('bi-building', 'Building')], default='bi-stars', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name'], 'verbose_name_plural': 'Facilities'},
        ),
        migrations.CreateModel(
            name='FacilityImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='facilities/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('facility', models.ForeignKey(on_delete=models.CASCADE, related_name='images', to='core.facility')),
            ],
            options={'ordering': ['order']},
        ),
        migrations.CreateModel(
            name='ManagementTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('role', models.CharField(max_length=150)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='team/')),
                ('bio', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order', 'name']},
        ),
    ]
