import os

from luigi import ExternalTask, Parameter, Task, LocalTarget, format
from luigi.contrib.s3 import S3Target, S3Client
from ..hash_str import get_csci_salt

image_name = 'Waluigi.jpeg'
model_name = 'udnie.pth'

class ContentImage(ExternalTask):
    IMAGE_ROOT = 's3://pset4data/pset_4/images'  # Root S3 path, as a constant

    # Name of the image
    image = Parameter('Waluigi.jpeg')  # Filename of the image under the root s3 path

    def output(self):
        client = S3Client(get_csci_salt(keyword='aws_access_key_id',convert_to_bytes="no"),
                                        get_csci_salt('aws_secret_access_key',convert_to_bytes="no"))
        return S3Target('s3://pset4data/pset_4/images/Waluigi.jpeg',
                        client=client,
                        format=format.Nop)  # return the S3Target of the image


class SavedModel(ExternalTask):
    MODEL_ROOT = 's3://pset4data/pset_4/saved_models/'

    model = Parameter('udnie.pth') # Filename of the model

    def output(self):
        return S3Target('s3://pset4data/pset_4/saved_models/udnie.pth', format=format.Nop)
        # return the S3Target of the model

class DownloadModel(Task):
    S3_ROOT = 's3://pset4data/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'saved_models'

    model = Parameter('udnie.pth') #luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally
        return SavedModel()

    def output(self):
        targetpath = os.path.join(os.getcwd(), 'data/')
        target = os.path.join(targetpath, model_name)

        return LocalTarget(target, format=format.Nop)

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.input().open('r') as f:
            result = f.read()
            with self.output().open('wb') as outfile:
                outfile.write(result)

class DownloadImage(Task):
    S3_ROOT = 's3://pset4data/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'images'

    image = Parameter('Waluigi.jpeg') # Luigi parameter

    def requires(self):
        # Depends on the ContentImage ExternalTask being complete
        return ContentImage()

    def output(self):
        targetpath = os.path.join(os.getcwd(), 'data/')
        target = os.path.join(targetpath, image_name)

        return LocalTarget(target, format=format.Nop)

    # TODO - replace with atomicwrite
    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.input().open('r') as f:
            result = f.read()
            with self.output().open('wb') as outfile:
                outfile.write(result)
