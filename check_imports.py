modules = [
    'app.database',
    'app.models',
    'app.schemas',
    'app.repositories',
    'app.deps',
    'app.security',
    'app.main'
]

for m in modules:
    try:
        __import__(m)
        print('OK', m)
    except Exception as e:
        print('ERROR importing', m, repr(e))
        raise
