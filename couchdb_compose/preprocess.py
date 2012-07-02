import coffeescript

from execjs import ProgramError

DOT_COFFEE = '.coffee'

def compile_coffeescript(data):
    try:
        data = coffeescript.compile(data, bare=True)
    except ProgramError as exc:
        print repr(data)
        raise SyntaxError(exc.args[0])
    return data.strip()


def commonjs_to_coffeescript(path, name, data):
    if isinstance(data, str) and name.endswith(DOT_COFFEE):
        return name[:-len(DOT_COFFEE)], compile_coffeescript(data)


def attachment_to_coffeescript(path, name, info):
    if path==('_attachments',) and name.endswith(DOT_COFFEE):
        info = dict(info,
            data=compile_coffeescript(info['data']),
            content_type="application/javascript",
        )
        return name.replace(DOT_COFFEE, '.js') , info


def preprocess(data, path, processors):
    for k, v in list(data.items()):
        for p in processors:
            try:
                result = p(path, k, v)
            except:
                print 'fail', path, k
                raise
            if result:
                # replace v here so we dont process
                new_k, v = result
                data.pop(k)
                data[new_k] = v

            if isinstance(v, dict):
                preprocess(v, path + (k,), processors)


preprocessors = [
    commonjs_to_coffeescript,
    attachment_to_coffeescript,
]

def run_preprocessors(composer):
    preprocess(composer.doc, (), preprocessors)
