
def ellipsize(doc):
    if isinstance(doc, (str, unicode)):
        return '...' if '\n' in doc else doc
    elif isinstance(doc, list):
        return [ellipsize(item) for item in doc]
    elif doc is not None:
        return dict((key, ellipsize(value)) for key, value in doc.items())
