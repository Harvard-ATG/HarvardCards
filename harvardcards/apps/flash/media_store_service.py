import os
import hashlib
import mimetypes

from PIL import Image, ImageFile
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from harvardcards.apps.flash.models import MediaStore


MEDIA_ROOT = settings.MEDIA_ROOT

class MediaStoreService:
    """Class to manage reading and writings files to the local media store."""

    def __init__(self, *args, **kwargs):
        file = kwargs.get('file', None)

        if isinstance(file, basestring):
            if os.path.exists(file):
                file_object = open(file, 'r')
                file_name = os.path.split(file)[1]
                file_type = mimetypes.guess_type(file_name)[0]
                file_size = os.path.getsize(file)
                file = UploadedFile(
                    file=file_object, 
                    name=file_name, 
                    content_type=file_type, 
                    size=file_size, 
                    charset=None
                )

        if not isinstance(file, UploadedFile):
            raise Exception("Error handling file: MediaStoreService expects UploadedFile")

        self._file_md5hash = None
        self.file = file
        self._createBaseDirs()

    def save(self, type=None):
        """Saves the media store."""

        if self.fileRecordExists():
            store = self.lookupFileRecord()
        else:
            self.writeFile()
            self.process(type)
            self.link(type)
            store = self.createFileRecord()
            store.save()

        return store

    def process(self, type=None):
        if type == 'I':
            self._processResizeImage()

    def link(self, type=None):
        file_name = self.storeFileName()

        # link to the original media file
        original_source_path = os.path.join('..', '..', self.storeFilePath('original'))
        original_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'original', file_name))
        if not os.path.lexists(original_link_path):
            os.symlink(original_source_path, original_link_path)

        if type == 'I':
            # link to the large thumbnail file
            large_source_path = os.path.join('..', '..', self.storeFilePath('thumb-large'))
            large_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-large', file_name))
            if not os.path.lexists(large_link_path):
                os.symlink(large_source_path, large_link_path)

            # link to the small thumbnail file
            small_source_path = os.path.join('..', '..', self.storeFilePath('thumb-small'))
            small_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-small', file_name))
            if not os.path.lexists(small_link_path):
                os.symlink(small_source_path, small_link_path)


    def writeFile(self):
        file = self.file
        file_name = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        with open(file_name, 'wb+') as dest:
            if file.multiple_chunks:
                for c in file.chunks():
                    dest.write(c)
            else:
                dest.write(file.read())

    def fileHash(self):
        if self._file_md5hash:
            return self._file_md5hash

        m = hashlib.md5()
        if self.file.multiple_chunks:
            for chunk in self.file.chunks():
                m.update(chunk)
        else:
            m.update(self.file.read())

        self._file_md5hash = m.hexdigest()

        return self._file_md5hash

    def createFileRecord(self):
        return MediaStore(
            file_name=self.storeFileName(),
            file_size=self.file.size,
            file_type=self.file.content_type,
            file_md5hash=self.fileHash()
        )

    def fileRecordExists(self):
        return MediaStore.objects.filter(file_md5hash=self.fileHash()).exists()

    def lookupFileRecord(self):
        return MediaStore.objects.filter(file_md5hash=self.fileHash())[0]

    def storeDir(self):
        return 'store'

    def storeFileDir(self):
        return os.path.join(self.storeDir(), self.fileHash())

    def storeFileName(self):
        file_extension = os.path.splitext(self.file.name)[1]
        return self.fileHash() + file_extension.lower()

    def storeFilePath(self, path):
        return os.path.join(self.storeFileDir(), path, self.storeFileName())

    def _createBaseDirs(self):
        file_paths = [
            MEDIA_ROOT,
            os.path.join(MEDIA_ROOT, self.storeDir()),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'original'),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-large'),
            os.path.join(MEDIA_ROOT, self.storeDir(), 'thumb-small'),
            os.path.join(MEDIA_ROOT, self.storeFileDir()),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'original'),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'thumb-large'),
            os.path.join(MEDIA_ROOT, self.storeFileDir(), 'thumb-small'),
        ]
        for p in file_paths:
            if not os.path.exists(p):
                os.mkdir(p)

    def _processResizeImage(self):
        """
        Resizes an uploaded image. Saves both the original, thumbnail, and resized versions.
        """

        original_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        thumb_large_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-large')))
        thumb_small_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-small')))

        img = Image.open(original_path)

        # create large thumbnail
        width, height = img.size
        new_height = 600;
        max_width = 1000;
        if height > new_height:
            new_width = width*new_height/float(height);
            img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            img_anti.save(thumb_large_path)
        else:
            if width > max_width:
                new_height = height*max_width/float(width)
                img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
                img_anti.save(thumb_large_path)
            else:
                img.save(thumb_large_path)

        # create small thumbnail
        t_height = 150
        t_width = width*t_height/float(height)
        img_thumb = img.resize((int(t_width), int(t_height)), Image.ANTIALIAS)
        img_thumb.save(thumb_small_path)

    @classmethod
    def getAbsPathToStore(cls):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store'))

    @classmethod
    def getAbsPathToOriginal(cls, file_name):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store', 'original', file_name))

