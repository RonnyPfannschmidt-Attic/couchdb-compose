import yaml


def path_2_attrchain(path):
    if path.endswith('.yml'):
        path = path[:-4]

    return path.split('/')


def load_objects(composer):
    #XXX: conflicts

    listing = composer.getlist('load')
    paths = []
    for item in listing:
        if '*' in item:
            raise NotImplemented
        else:
            paths.append(item)

    for path in paths:
        objectpath = path_2_attrchain(path)
        path = composer.path.join(path)
        input = path.read()
        if path.ext == '.yml':
            data = yaml.load(input)
        else:
            data = input

        composer.push(objectpath, data)


