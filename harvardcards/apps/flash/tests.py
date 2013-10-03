from django.test import TestCase
from harvardcards.apps.flash.models import Collection

class CollectionTest(TestCase):
    def test_collection(self):
        title = "title of card"
        des = "nothing in description"
        collection = Collection(title, des)
        outp = "{description: '" + des + "', title: '" + title + "'}"
        self.assertEqual(collection.export, outp)
