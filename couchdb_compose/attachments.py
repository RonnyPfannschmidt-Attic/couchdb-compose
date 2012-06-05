

def add_attachments(composer):
    #XXX: renames
    attachments = composer.config.get('attachments')
    for attachment in attachments:
        if isinstance(attachment, str):
            for path in composer.path.visit(attachment):
                composer.push_attachment(path)
        else:
            for prefix, maybe_globs in attachment.items():
                newpath = composer.path.join(prefix)
                if not newpath.check(dir=1):
                    print '! attachments below', prefix, 'for', maybe_globs, 'not found'
                    continue
                if not isinstance(maybe_globs, (list, tuple)):
                    maybe_globs = [maybe_globs]

                for glob in maybe_globs:
                    for path in newpath.visit(glob):
                        composer.push_attachment(path)
