from grid5000 import Grid5000

def login(username: str, password: str) -> Grid5000:
    """Login on the grid5000 network with a user. Return the g5k object.

    Args:
        username (str): the username to connect with
        password (str): the password for the given user
    """
    
    return Grid5000(username=username, password=password)
