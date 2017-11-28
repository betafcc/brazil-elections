import os.path
import posixpath
from uuid import uuid4
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor as Pool

from PIL import Image

from .util import DATA_ROOT, absjoin, load_json, to_json


SRC        = absjoin(DATA_ROOT, 'interim', 'candidatos_imgs.json')
THUMBNAILS = absjoin(DATA_ROOT, 'deliver', 'thumbnails')
INDEX      = absjoin(DATA_ROOT, 'interim', 'candidatos_imgs_relative.json')
REL_PREFIX = './data/thumbnails'




def generate_path(base_path, url):
    return absjoin(base_path, str(uuid4()) + posixpath.splitext(url)[1])


def download_thumbnail(url, path):
    with urlopen(url) as fp:
        img = Image.open(fp)

    img.thumbnail((128, 128))
    img.save(path)


def download_and_set_one(acc, k, url):
    path = generate_path(THUMBNAILS, url)
    download_thumbnail(url, path)
    acc[k] = posixpath.join(REL_PREFIX, os.path.basename(path))


if __name__ == '__main__':
    candidatos = load_json(SRC)

    acc = {}
    with Pool(10) as executor:
        for k, url in candidatos.items():
            if url:
                executor.submit(download_and_set_one, acc, k, url)
            else:
                acc[k] = url


    to_json(acc, INDEX)
