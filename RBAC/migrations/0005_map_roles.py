from django.db import migrations

def map_roles(apps, schema_editor):
    UserProfile = apps.get_model('RBAC', 'UserProfile')
    Role = apps.get_model('RBAC', 'Role')
    for profile in UserProfile.objects.all():
        if isinstance(profile.role, str):
            try:
                role_obj = Role.objects.get(role=profile.role)
                profile.role = role_obj
                profile.save()
            except Role.DoesNotExist:
                pass

class Migration(migrations.Migration):
    dependencies = [
        ('RBAC', '0004_alter_rolepermission_unique_together_and_more'),
    ]

    operations = [
        migrations.RunPython(map_roles),
    ]
