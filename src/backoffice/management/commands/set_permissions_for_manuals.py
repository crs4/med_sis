from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from geonode.documents.models import Document


class Command(BaseCommand):
    help = "Set document read/download permissions for registered users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pk",
            nargs="+",
            type=int,
            required=True,
            help="One or more document primary keys",
        )

    def handle(self, *args, **options):
        group_name = getattr(
            settings,
            "DOCUMENT_READ_DOWNLOAD_GROUP",
            "registered-members",
        )

        if not Group.objects.filter(name=group_name).exists():
            raise CommandError(f"Group not found: {group_name}")

        for pk in options["pk"]:
            try:
                document = Document.objects.get(pk=pk)
            except Document.DoesNotExist:
                self.stderr.write(f"Document {pk} not found")
                continue

            owner = document.owner
            if owner is None:
                self.stderr.write(
                    f"Document {pk} has no owner; skipped"
                )
                continue

            perm_spec = {
                "users": {
                    owner.username: [
                        "view_resourcebase",
                        "download_resourcebase",
                        "change_resourcebase",
                        "delete_resourcebase",
                        "change_resourcebase_permissions",
                        "change_resourcebase_metadata",
                        "publish_resourcebase",
                    ]
                },
                "groups": {
                    group_name: [
                        "view_resourcebase",
                        "download_resourcebase",
                    ]
                },
            }

            result = document.set_permissions(perm_spec)

            if result is not True:
                self.stderr.write(
                    f"Permissions not confirmed for document {pk}"
                )
                continue

            self.stdout.write(
                self.style.SUCCESS(
                    f"Document {pk}: permissions updated"
                )
            )
            