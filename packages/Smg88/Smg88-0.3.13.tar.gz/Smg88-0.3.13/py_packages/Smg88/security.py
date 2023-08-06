"""This module contains the security-related functions for the Smg88 package.

Most of the objects in this module have their metaclass being of this class, namely 'Security'
This means that each binding (such as methods or properties) each have a security level from 0 to 69, where 0 is the most secure and 69 is the least secure.
"""


class Security(type, metaclass=type):
    """This class is designed to be the metaclass of all objects following the Security design pattern.

    This makes the class only accessable to allowed security levels, with any other level than 69 needing confirmation
    """
    # TODO DESIGN then implement the security features proposed in the above docstrings
    ...
