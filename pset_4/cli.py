from luigi import build
from .tasks.data import ContentImage, DownloadImage, DownloadModel
from .tasks.stylize import Stylize


def main():
    build([
        Stylize(
            model='rain_princess.pth',
            image='luigi.jpeg'
        )], local_scheduler=True)
