from django.contrib.staticfiles.storage import StaticFilesStorage


class YDcommonFileSystemStorage(StaticFilesStorage):

    def post_process(self, *args, **kwargs):
        print self
        print args
        print kwargs
