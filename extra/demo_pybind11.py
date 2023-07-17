# Import magic
try:
  import database_manager
except ImportError as e:
  print(f"Importing the shared library 'database_manager' did not work.")
  print(f"Is (a link to) the shared library 'database_manager.____.so' in the same directory as this python script?")
  print(f"The import caused the following exception '{e}'")
  print(f"Exiting")
  exit(1)
else:
  print(f"Importing the shared library 'database_manager' did work.")


import pydoc


def main():
  print(f"Module name: '{database_manager.__doc__}'")


if __name__ == '__main__':
  main()
