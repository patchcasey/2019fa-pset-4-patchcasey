from luigi import build
from .tasks.data import ContentImage, DownloadImage


def main():
    build([
        DownloadImage(
            image='luigi.jpeg'
        )], local_scheduler=True)
