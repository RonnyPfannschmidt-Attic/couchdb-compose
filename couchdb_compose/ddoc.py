import yaml


def path_2_attrchain(path):
    if path.endswith('.yml'):
        path = path[:-4]

    return path.split('/')


def load_objects(composer):
    #XXX: conflicts

    listing = composer.config['load']
    paths = []
    for item in listing:
        print item
        if '*' in item:
            raise NotImplemented
        else:
            paths.append(item)

    for path in paths:
        objectpath = path_2_attrchain(path)
        path = composer.path.join(path)
        with path.open() as fp:
            data = yaml.load(fp)

        composer.push(objectpath, data)


