"""This command is intended for one-time use to migrate previously uploaded
files (images, audio, etc) to the new MediaStore model."""

from django.core.management.base import BaseCommand, CommandError

from harvardcards.settings.common import MEDIA_ROOT 
from flash.services import handle_uploaded_media_file
from flash.models import Cards_Fields

import os
import re

class Command(BaseCommand):
    help = 'Converts files to the new MediaStore model.'

    def handle(self, *args, **kwargs):
        cards_fields = Cards_Fields.objects.all().select_related('field')
        pathre = re.compile('^\d+_\d+\/')
        count = 0
        fieldmap = {}

        for cf in cards_fields:
            # skip empty fields or fields that don't match "[DECK_ID]_[COLLECTION_ID]/"
            if cf.value == '' or not pathre.match(cf.value):
                continue
            
            # check to see if there's an original file, which would be located here 
            # if it was previously resized
            filepath = os.path.abspath(os.path.join(MEDIA_ROOT, 'originals', cf.value))
            if not os.path.exists(filepath):
                # otherwise it's probably an audio file, which would be here
                filepath = os.path.abspath(os.path.join(MEDIA_ROOT, cf.value))

            # add the file to the media store and save the new field value
            if os.path.exists(filepath):
                result = handle_uploaded_media_file(filepath, cf.field.field_type)

                logstr = "cf.id=%s cf.field.field_type=%s cf.value=%s filepath=%s result=%s"
                self.stdout.write(logstr % (cf.id, cf.field.field_type, cf.value, filepath, result))

                fieldmap[cf.value] = result
                count += 1

                cf.value = result
                cf.save()

        self.stdout.write("Total converted: %d" % count)
        self.stdout.write("Updated values: %s" % fieldmap)
        self.stdout.write("Done!")
