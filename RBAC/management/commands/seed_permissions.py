from django.core.management.base import BaseCommand
from RBAC.models import Role, Permission, RolePermission

class Command(BaseCommand):
    help = "Assign permissions to roles"

    def handle(self, *args, **options):
        admin_role = Role.objects.get(role = "admin")
        editor_role = Role.objects.get(role="editor")
        viewer_role = Role.objects.get(role="viewer")

        admin_perm = ["add_blog", "view_blog", "delete_blog", "view_blog",
                      "add_domestic_trip", "view_domestic_trip", "delete_domestic_trip",
                      "add_international_trip", "view_international_trip", "delete_international_trip",
                      "add_service", "view_service", "delete_service", "update_service"]

        editor_perm = ["add_blog", "view_blog", "update_blog",
                       "add_domestic_trip", "view_domestic_trip", "update_domestic_trip",
                       "add_international_trip", "view_international_trip", "update_international_trip",
                       "add_service", "view_service", "update_service"]
        viewer_perm = ["view_blog", "view_domestic_trip", "view_international_trip", "view_service"]

        for perm_name in admin_perm:
            perm, _ = Permission.objects.get_or_create(name=perm_name)
            RolePermission.objects.get_or_create(role=admin_role, permission=perm)

        for perm_name in editor_perm:
            perm, _ = Permission.objects.get_or_create(name=perm_name)
            RolePermission.objects.get_or_create(role=editor_role, permission=perm)

        for perm_name in viewer_perm:
            perm, _ = Permission.objects.get_or_create(name=perm_name)
            RolePermission.objects.get_or_create(role=viewer_role, permission=perm)

        self.stdout.write(self.style.SUCCESS("Permissions assigned Successfully!!!"))