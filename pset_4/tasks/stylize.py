from neural_style.neural_style import stylize
import os

from luigi import ExternalTask, Parameter, Task, LocalTarget, format
from csci_utils import luigi as csci_luigi

image_name = 'luigi.jpeg'
model_name = 'udnie.pth'

class Stylize(Task):
    targetpath = os.path.join(os.getcwd(), 'data/')
    image_target = os.path.join(targetpath, image_name)
    model_target = os.path.join(targetpath, model_name)

    model = Parameter(model_target)
    image = Parameter(image_target)

    def requires(self):
        return {
            'image': csci_luigi.DownloadImage(),
            'model': csci_luigi.DownloadModel()
        }

    def output(self):
        # return SuffixPreservingLocalTarget of the stylized image
        targetpath = os.path.join(os.getcwd(), 'data/')
        styled_image = os.path.join(targetpath, 'styled_image_Waluigi_udnie_test2.jpeg')
        return csci_luigi.SuffixPreservingLocalTarget(styled_image, format=format.Nop)

    def run(self):
        # For example
        inputs = self.input()
        # with self.output().temporary_path() as temp_output_path:
        class args:
            content_image = inputs['image'].path
            model = inputs['model'].path
            output_image = self.output().path
            cuda = 0
            content_scale = 1
            export_onnx = False

        stylize(args)

