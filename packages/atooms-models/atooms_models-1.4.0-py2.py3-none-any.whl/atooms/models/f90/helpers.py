import os

def _normalize_path(path):
    if not path.endswith('.f90'):
        path = path + '.f90'

    if os.path.exists(path):
        return path
    else:
        # Look in this module path
        dirname = os.path.dirname(__file__)
        full_path = os.path.join(dirname, path)
        if os.path.exists(full_path):
            return full_path
        else:
            raise ValueError('could not find source for {}'.format(path))


def _merge_source(*paths):
    """Merges `sources` into a unique source."""
    merged_src = ''
    for path in paths:
        # Check path existence
        source_path = _normalize_path(path)
        with open(source_path) as fh:
            src = fh.read()
        # Merge sources into a single one
        merged_src += src
    return merged_src
