

def add_attachments(composer):
    #XXX: renames
    attachments = composer.getlist('attachments')
    for attachment in attachments:
        if isinstance(attachment, str):
            for path in composer.path.visit(attachment):
                composer.add_attachment_from_file(path)
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
                        composer.add_attachment_from_file(path)
