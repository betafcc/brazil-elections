from os.path import dirname, abspath, join
import json


__dirname = dirname(__file__)


def absjoin(*args):
    return abspath(join(*args))


def load_json(path):
    with open(path, 'r') as fd:
        return json.load(fd,
                         encoding='utf-8')


def to_json(d, path, minify=False):
    with open(path, 'w') as fp:
        json.dump(d,
                  fp,
                  indent=2 if not minify else None,
                  sort_keys=True,
                  ensure_ascii=False,
                  )


DATA_ROOT = abspath(join(__dirname, '..', 'data'))
