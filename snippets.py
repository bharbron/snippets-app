import logging
import argparse
import sys
import psycopg2

logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet, hide, show):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Store snippet {!r}: {!r}; hide = {!r}, show = {!r}".format(name, snippet, hide, show))
    with connection, connection.cursor() as cursor:
      try:
        command = "insert into snippets values (%s, %s, %s)"
        cursor.execute(command, (name, snippet, hide))
      except psycopg2.IntegrityError as e:
        connection.rollback()
        if hide:
          command = "update snippets set message=%s, hidden=TRUE where keyword=%s"
        elif show:
          command = "update snippets set message=%s, hidden=FALSE where keyword=%s"
        else:
          command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet
  
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, returns None

    Returns the snippet.
    """
    logging.info("Retrieve snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
      command = "select message from snippets where keyword = %s"
      cursor.execute(command, (name,))
      row = cursor.fetchone()
    if not row:
      logging.warn("No snippet was found with that name.")
      return None
    logging.debug("Snippet retrieved successfully.")
    return row[0]
  
def remove(name):
    """
    Deletes the snippet with the given name
    
    Returns the name
    """
    logging.error("FIXME: Unimplemented - remove({!r})".format(name))
    return name
  
def catalog():
    """
    Fetches a list of all names from the snippets database
    
    Returns the names as a list
    
    Returns an empty list if there are no snippets in the database
    """
    logging.info("Retrieving catalog of snippet names")
    names = []
    with connection, connection.cursor() as cursor:
      command = "select keyword from snippets where not hidden order by keyword asc"
      cursor.execute(command)
      rows = cursor.fetchall()
      if rows:
        for row in rows:
          names.append(row[0])
    return names
  
def search(phrase):
    """
    Searches for snippets that contain the given phrase somewhere in their message

    Returns a list of tuples (snippet name and message) that contain the phrase
    
    Returns None if no snippets were found with the phrase
    """
    logging.info("Searching for snippets with phrase {!r}".format(phrase))
    with connection, connection.cursor() as cursor:
      command = "select keyword, message from snippets where message like '%{}%' and not hidden".format(phrase)
      cursor.execute(command)
      rows = cursor.fetchall()
    if not rows:
      logging.info("No snippets were found with that phrase.")
      return None
    logging.debug("Search found snippets")
    return rows
  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    group = put_parser.add_mutually_exclusive_group()
    group.add_argument("--hide", help="Sets the hidden flag on the snippet", action="store_true")
    group.add_argument("--show", help="Removes the hidden flag from the snippet", action="store_true")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="List all snippet names in the database")
    
    # Subparse for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Searches for snippets with the given phrase somewhere in their message")
    search_parser.add_argument("phrase", help="The phrase to search for")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
      name, snippet = put(**arguments)
      print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
      snippet = get(**arguments)
      if snippet:
        print("Retrieved snippet: {!r}".format(snippet))
      else:
        print "No snippet was found with that name."
    elif command == "catalog":
      names = catalog()
      print "The snippets database contains the following names:"
      for name in names:
        print name
    elif command == "search":
      snippets = search(**arguments)
      if snippets:
        print "Found the following snippets:"
        print 'Name\tMessage'
        print '-----------------'
        for snippet in snippets:
          print '{}\t{}'.format(snippet[0], snippet[1])
      else:
        print "No snippets were found with that phrase."
      

if __name__ == "__main__":
    main()