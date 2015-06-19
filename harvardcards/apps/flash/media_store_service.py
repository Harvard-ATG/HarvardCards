import os
import hashlib
import mimetypes
import tempfile

from PIL import Image, ImageFile
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from harvardcards.apps.flash.models import MediaStore

MEDIA_ROOT = settings.MEDIA_ROOT
#MEDIA_STORE_BACKEND = settings.MEDIA_STORE_BACKEND
MEDIA_STORE_BACKEND = "s3" # s3|file

class MediaStoreService:
    """Class to manage media file storage."""

    def __init__(self, *args, **kwargs):
        file = kwargs.get('file', None)
        file_type = kwargs.get('file_type', None)

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
        self.file_type = file_type

        if MEDIA_STORE_BACKEND.lower() == "file":
            self.store = MediaStoreFile(self)
        elif MEDIA_STORE_BACKEND.lower() == "s3":
            self.store = MediaStoreS3(self)

    def save(self):
        self.store.save()

    def createRecord(self):
        return MediaStore(
            file_name=self.storeFileName(),
            file_size=self.file.size,
            file_type=self.file.content_type,
            file_md5hash=self.getFileHash()
        )

    def recordExists(self):
        return MediaStore.objects.filter(file_md5hash=self.getFileHash()).exists()

    def lookupRecord(self):
        return MediaStore.objects.filter(file_md5hash=self.getFileHash())[0]

    def getFileHash(self):
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

    def storeDir(self):
        return 'store'

    def storeFileDir(self):
        return os.path.join(self.storeDir(), self.getFileHash())

    def storeFileName(self):
        file_extension = os.path.splitext(self.file.name)[1]
        return self.getFileHash() + file_extension.lower()

    def storeFilePath(self, path):
        return os.path.join(self.storeFileDir(), path, self.storeFileName())

    def resizeImageLarge(self, input_file, output_file):
        print "input=%s output=%s" % (input_file, output_file)
        img = Image.open(input_file)
        width, height = img.size

        # create large thumbnail
        new_height = 600;
        max_width = 1000;
        if height > new_height:
            new_width = width*new_height/float(height);
            img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
            img_anti.save(output_file)
        else:
            if width > max_width:
                new_height = height*max_width/float(width)
                img_anti = img.resize((int(new_width), int(new_height)), Image.ANTIALIAS)
                img_anti.save(output_file)
            else:
                img.save(output_file)

    def resizeImageSmall(self, input_file, output_file):
        img = Image.open(input_file)
        width, height = img.size

        # create small thumbnail
        t_height = 150
        t_width = width*t_height/float(height)
        img_thumb = img.resize((int(t_width), int(t_height)), Image.ANTIALIAS)
        img_thumb.save(output_file)

    def writeFileTo(self, file_name):
        file = self.file
        with open(file_name, 'wb+') as dest:
            if file.multiple_chunks:
                for c in file.chunks():
                    dest.write(c)
            else:
                dest.write(file.read())

class MediaStoreFile:
    """Class to manage reading and writings files to the media store."""

    def __init__(self, mediaService):
        self.mediaService = mediaService
        self.createBaseDirs()

    def storeDir(self):
        return self.mediaService.storeDir()

    def storeFileDir(self):
        return self.mediaService.storeFileDir()

    def storeFileName(self):
        return self.mediaService.storeFileName()

    def storeFilePath(self, path):
        return self.mediaService.storeFilePath(path)

    def save(self):
        """Saves the media store."""
        file_type = self.mediaService.file_type
        if self.mediaService.recordExists():
            record = self.mediaService.lookupRecord()
        else:
            self.writeFile()
            self.process(file_type)
            self.link(file_type)
            record = self.mediaService.createRecord()
            record.save()
        return record

    def process(self, file_type=None):
        if file_type == 'I':
            self.processResizeImage()

    def link(self, file_type=None):
        file_name = self.storeFileName()

        # link to the original media file
        original_source_path = os.path.join('..', '..', self.storeFilePath('original'))
        original_link_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeDir(), 'original', file_name))
        if not os.path.lexists(original_link_path):
            os.symlink(original_source_path, original_link_path)

        if file_type == 'I':
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
        file_name = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        self.mediaService.writeFileTo(file_name)

    def createBaseDirs(self):
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

    def processResizeImage(self):
        """
        Resizes an uploaded image. Saves both the original, thumbnail, and resized versions.
        """

        original_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('original')))
        thumb_large_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-large')))
        thumb_small_path = os.path.abspath(os.path.join(MEDIA_ROOT, self.storeFilePath('thumb-small')))

        self.mediaService.resizeImageLarge(original_path, thumb_large_path)
        self.mediaService.resizeImageSmall(original_path, thumb_small_path)

    @classmethod
    def getAbsPathToStore(cls):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store'))

    @classmethod
    def getAbsPathToOriginal(cls, file_name):
        return os.path.abspath(os.path.join(MEDIA_ROOT, 'store', 'original', file_name))

class MediaStoreS3:
    """Class to manage reading and writings files to Amazon S3."""

    def __init__(self, mediaService):
        self.mediaService = mediaService
        self.conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_ACCESS_SECRET_KEY)
        self.bucket = self.conn.get_bucket(settings.AWS_S3_BUCKET)
        self.thumb_file_large = None
        self.thumb_file_small = None
        self.original_file = None

    def storeDir(self):
        return self.mediaService.storeDir()

    def storeFileDir(self):
        return self.mediaService.storeFileDir()

    def storeFileName(self):
        return self.mediaService.storeFileName()

    def storeFilePath(self, path):
        return self.mediaService.storeFilePath(path)

    def save(self):
        """Saves the media store."""
        file_type = self.mediaService.file_type
        if self.mediaService.recordExists():
            record = self.mediaService.lookupRecord()
        else:
            self.process(file_type)
            self.saveToBucket()
            record = self.mediaService.createRecord()
            record.save()
        return record

    def process(self, file_type):
        if file_type == "I":
            self.processResizeImage()

    def processResizeImage(self):
        ext = os.path.splitext(self.mediaService.file.name)[1]
        self.original_file = tempfile.NamedTemporaryFile('r+', -1, ext)
        self.thumb_file_large = tempfile.NamedTemporaryFile('r+', -1, ext)
        self.thumb_file_small = tempfile.NamedTemporaryFile('r+', -1, ext)

        self.mediaService.writeFileTo(self.original_file.name)
        self.original_file.seek(0)

        self.mediaService.resizeImageLarge(self.original_file.name, self.thumb_file_large)
        self.thumb_file_large.seek(0)

        self.mediaService.resizeImageSmall(self.original_file.name, self.thumb_file_small)
        self.thumb_file_small.seek(0)

    def saveToBucket(self):
        original = Key(self.bucket)
        original.key = self.storeFilePath('original')
        original.set_contents_from_string(self.original_file.read())

        thumb_large = Key(self.bucket)
        thumb_large.key = self.storeFilePath('thumb-large')
        thumb_large.set_contents_from_string(self.thumb_file_large.read())

        thumb_small = Key(self.bucket)
        thumb_small.key = self.storeFilePath('thumb-small')
        thumb_small.set_contents_from_string(self.thumb_file_small.read())

        print original.generate_url(expires_in=0, query_auth=False)
