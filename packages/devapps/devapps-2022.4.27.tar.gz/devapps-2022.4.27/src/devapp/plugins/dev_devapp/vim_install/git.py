from devapp.app import FLG, app, system, do
from dev_devapp import vim_install

g = getattr


def clone(resource):
    r = resource
    url = g(FLG, r.typ + '_url')
    if not url:
        return
    if url.startswith('gh:'):
        url = 'git@github.com:' + url[3:]
    if not url.endswith('.git'):
        url += '.git'
    D = r.pth
    while True:
        dpth = '--depth=1' if r.version == 'latest' else ''
        cmd = f'git clone {dpth} "{url}" "{D}"'
        err = do(system, cmd, no_fail=True)
        if not err:
            break
        if url.startswith('git@'):
            a, b = url[4:].split(':', 1)
            url = f'https://{a}/{b}'
            app.info('Trying https...', url=url)
            continue
        app.die('Could not git clone', url=url)
    if not r.version == 'latest':
        v = r.version
        cmd = f'cd "{D}" && git checkout "{v}"'
        vim_install.exec_(cmd, 'setting version')
