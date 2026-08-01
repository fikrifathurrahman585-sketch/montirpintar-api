from app.loader import load_taxonomy


taxonomy = load_taxonomy()


def has_system(system):

    return system in taxonomy
