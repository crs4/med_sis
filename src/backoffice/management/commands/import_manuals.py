import uuid
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from geonode.documents.models import Document
from geonode.resource.registry import resource_manager_registry

OWNER_PERMISSIONS = [
    'view_resourcebase', 'download_resourcebase', 'change_resourcebase',
    'delete_resourcebase', 'change_resourcebase_permissions',
    'change_resourcebase_metadata', 'publish_resourcebase',
]


class Command(BaseCommand):
    help = 'Import a local GeoNode document and restrict read/download to a registered group.'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True)
        parser.add_argument('--title', required=True)
        parser.add_argument('--owner', default='admin')
        parser.add_argument('--group', default='registered-members')
        parser.add_argument('--skip-existing', action='store_true')

    def handle(self, *args, **options):
        path = Path(options['file'])
        if not path.is_file():
            raise CommandError(f'File not found inside Django container: {path}')

        User = get_user_model()
        try:
            owner = User.objects.get(username=options['owner'])
        except User.DoesNotExist:
            raise CommandError(f"Owner not found: {options['owner']}")
        group = options['group']
        if not Group.objects.filter(name=group).exists():
            raise CommandError(f'Group not found: {group}')

        # The title is an operational deduplication key for this initializer.
        # Check for ambiguous titles rather than updating an arbitrary resource.
        existing = list(Document.objects.filter(title=options['title'])[:2])
        if len(existing) > 1:
            raise CommandError(f"Multiple documents have title {options['title']!r}; resolve duplicates manually")
        if existing and not options['skip_existing']:
            raise CommandError(f"Document title already exists: {options['title']!r}; use --skip-existing")

        if existing:
            document = existing[0]
            self.stdout.write(f'EXISTING pk={document.pk} uuid={document.uuid} title={document.title}')
        else:
            # Use an existing Document instance to resolve the installed GeoNode manager.
            # The registry may also support get_for_model; get_for_instance was tested.
            reference = Document.objects.first()
            if reference is None:
                raise CommandError('No existing Document to resolve manager; initialize via an existing resource or adapt registry lookup')
            manager = resource_manager_registry.get_for_instance(reference)
            document = manager.create(
                str(uuid.uuid4()),
                file=str(path),
                user=owner,
                defaults={'title': options['title'], 'owner': owner},
            )
            self.stdout.write(f'IMPORTED pk={document.pk} uuid={document.uuid} title={document.title}')

        # Preserve the document's actual owner, including on existing resources.
        actual_owner = document.owner
        if actual_owner is None:
            raise CommandError(f'Document {document.pk} has no owner')
        perm_spec = {
            'users': {actual_owner.username: OWNER_PERMISSIONS},
            'groups': {group: ['view_resourcebase', 'download_resourcebase']},
        }
        if document.set_permissions(perm_spec) is not True:
            raise CommandError(f'Permission update not confirmed for document pk={document.pk}')
        document.refresh_from_db()
        info = document.get_all_level_info()
        granted = {g.name: set(perms) for g, perms in info['groups'].items()}
        expected = {'view_resourcebase', 'download_resourcebase'}
        if granted.get(group) != expected or 'anonymous' in granted:
            raise CommandError(f'Unexpected group permissions for pk={document.pk}: {granted}')
        self.stdout.write(self.style.SUCCESS(f'OK pk={document.pk} uuid={document.uuid} group={group}'))
