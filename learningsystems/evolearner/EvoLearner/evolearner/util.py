import re


def get_full_iri(x):
    return x.namespace.base_iri + x.name


def escape(name: str):
    name = name.split(".")[-1]
    name = re.sub(r'\W+', '', name)
    return name
