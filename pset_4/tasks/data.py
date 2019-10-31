import os

from luigi import ExternalTask, Parameter, Task, LocalTarget
from luigi.contrib.s3 import S3Target, S3Client
from ..hash_str import get_csci_salt

image_name = 'luigi.jpeg'

class ContentImage(ExternalTask):
    IMAGE_ROOT = 's3://pset4data/pset_4/images'  # Root S3 path, as a constant

    # Name of the image
    image = Parameter('luigi.jpeg')  # Filename of the image under the root s3 path

    def output(self):
        client = S3Client(get_csci_salt(keyword='aws_access_key_id',convert_to_bytes="no"),
                                        get_csci_salt('aws_secret_access_key',convert_to_bytes="no"))
        return S3Target('s3://pset4data/pset_4/images/luigi.jpeg', client=client)  # return the S3Target of the image


class SavedModel(ExternalTask):
    MODEL_ROOT = 's3://pset4data/pset_4/saved_models/'

    model = Parameter('rain_princess.pth') # Filename of the model

    def output(self):
        return S3Target('s3://pset4data/pset_4/saved_models/rain_princess.pth')
        # return the S3Target of the model

# class DownloadModel(Task):
#     S3_ROOT = 's3://pset4data/'
#     #TODO - maybe change location of folder or this directory?
#     LOCAL_ROOT = os.path.abspath('data')
#     SHARED_RELATIVE_PATH = 'saved_models'
#
#     model = ... #luigi parameter
#
#     def requires(self):
#         # Depends on the SavedModel ExternalTask being complete
#         # i.e. the file must exist on S3 in order to copy it locally
#         return SavedModel(self)
#
#     def output(self):
#
#
#     def run(self):
#         # Use self.output() and self.input() targets to atomically copy
#         # the file locally!

class DownloadImage(Task):
    S3_ROOT = 's3://pset4data/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'images'

    image = Parameter('luigi.jpeg') # Luigi parameter

    def requires(self):
        # Depends on the ContentImage ExternalTask being complete
        return ContentImage(self)

    def output(self):
        targetpath = os.path.join(os.getcwd(), "../..", 'data/')
        target = os.path.join(targetpath, image_name)

        return LocalTarget(target)

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!

        writing = self.input()
        outfile = self.output().open('w')
        print(outfile)



        # for input in self.input():
        #     print("test")
        #     with input.open() as f:
        #         result = f
        # if result:
        #     out_file = self.output().open('w')
        #     out_file.write(input)
