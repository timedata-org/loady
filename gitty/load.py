from . import raw, whitelist


def _guess_name(names, filename, url):
    if len(names) == 1:
        return names[0]

    if filename in names:
        return filename

    def canonical(symbol):
        return symbol.lower().replace('_', '')

    matches = [n for n in names if canonical(n) == canonical(filename)]
    if len(matches) == 1:
        return matches[0]

    raise ValueError('No member specified in %s' % url)


def load(url, use_whitelist=True, whitelist_prompt=True, request=raw.request):
    """
    Read a single Python file in as code and extract members from it.

    Args:
        url: a URL looking like
             https://github.com/foo/bar/blob/master/bibliopixel/myfile.MyClass

        use_whitelist: if true, make sure that the provider, user and project
                       are whitelisted before downloading code.

        whitelist_prompt: if true, prompt user to add code to the whitelist;
                          otherwise throw an exception if code is not
                          whitelisted.
    """
    slash = url.rfind('/')
    url_root, filepath = url[:slash + 1], url[slash + 1:]
    filename, *python_path = filepath.split('.')

    if use_whitelist:
        protocol, nothing, provider, user, project = url_root.split('/', 5)
        if not nothing:
            raise ValueError('Invalid URL %s' % url_root)

        entry = [provider, user, project]
        whitelist.check_or_prompt_to_add(entry, whitelist_prompt)

    file_url = url_root + filename + '.py'
    source = request(file_url, False)
    compiled = compile(source, file_url, mode='exec')
    local = {}
    exec(compiled, globals(), local)

    try:
        names = local['__all__']
    except KeyError:
        names = [k for k in local if not k.startswith('_')]

    if python_path and python_path[0] == 'py':
        python_path.pop(0)

    first, *rest = python_path or [_guess_name(names, filename, url)]
    try:
        result = local[first]
    except:
        raise AttributeError(first)

    for r in rest:
        result = getattr(result, r)

    return result
