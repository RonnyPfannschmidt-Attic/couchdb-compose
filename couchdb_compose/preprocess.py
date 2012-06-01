import coffeescript

from execjs import ProgramError

DOT_COFFEE = '.coffee'

def commonjs_to_coffeescript(path, name, data):
    if isinstance(data, str) and name.endswith(DOT_COFFEE):
        try:
            data = coffeescript.compile(data, bare=True)
        except ProgramError, e:
            print repr(data)
            raise SyntaxError(e.args[0])
        return name[:-len(DOT_COFFEE)], data

preprocessors = [commonjs_to_coffeescript]


def preprocess(data, path, processors):
    for k, v in data.items():
        for p in processors:
            try:
                result = p(path, k, v)
            except:
                print 'fail', path, k
                raise
            if result:
                # replace v herre so we dont process 
                new_k, v = result
                data.pop(k)
                data[new_k] = v

            if isinstance(v, dict):
                preprocess(v, path + (k,), processors)


def run_preprocessors(composer):
    preprocess(composer.doc, (), preprocessors)
