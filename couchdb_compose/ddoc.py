import yaml


def path_2_attrchain(path):
    if path.endswith('.yml'):
        path = path[:-4]

    return path.split('/')


def do_glob(match, basepath):
    for item in basepath.visit(match):
        yield basepath.bestrelto(item)


def load_objects(composer):
    #XXX: conflicts

    listing = composer.config['load']
    paths = []
    for item in listing:
        if '*' in item:
            paths.extend(do_glob(item, composer.path))
        else:
            paths.append(item)

    for path in paths:
        objectpath = path_2_attrchain(path)
        path = composer.path.join(path)
        with path.open() as fp:
            data = yaml.load(fp)

        composer.push(objectpath, data)


