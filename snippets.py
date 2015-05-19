import logging

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
  
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, inform the user no snippet of that name exists

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
  
def remove(name):
    """
    Deletes the snippet with the given name
    
    Returns the name
    """
    logging.error("FIXME: Unimplemented - remove({!r})".format(name))
    return name
    