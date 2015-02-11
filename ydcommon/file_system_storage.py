from django.core.files.storage import FileSystemStorage


class YDcommonFileSystemStorage(FileSystemStorage):

    def post_process(self, *args, **kwargs):
        print self
        print args
        print kwargs
        return super(YDcommonFileSystemStorage, self).post_process(*args, **kwargs)
