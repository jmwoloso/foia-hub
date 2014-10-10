from django.test import SimpleTestCase

from foia_hub.models import Agency


class AgencyTests(SimpleTestCase):
    def test_examples_field(self):
        """Verify that we can treat a JSONField as a list"""
        agency = Agency(name='Dr. Suess',
                        examples=['Thing one', 'Thing two', 'Red Fish'])
        agency.save()
        # Serialized to the DB and back again
        retrieved = Agency.objects.get(pk=agency.pk)
        self.assertEqual(retrieved.examples,
                         ['Thing one', 'Thing two', 'Red Fish'])
        agency.delete()