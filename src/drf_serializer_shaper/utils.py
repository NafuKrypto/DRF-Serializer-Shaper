def build_nested_tree(fields):
    tree = {}
    for field in fields:
        parts = field.split("__")
        current = tree
        for part in parts:
            current = current.setdefault(part, {})
    return tree


def flatten_tree(tree, prefix=None):
    paths = []
    for key, subtree in tree.items():
        current = [key] if not prefix else prefix + [key]
        if subtree:
            paths.extend(flatten_tree(subtree, current))
        else:
            paths.append(current)
    return paths