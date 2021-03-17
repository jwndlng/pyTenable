'''
servers
=====

The following methods allow for interaction into the Nessus Professional

Methods available on ``nessus.servers``:

.. rst-class:: hide-signature
.. autoclass:: ServerAPI

    .. automethod:: status
'''

from .base import NessusEndpoint

class ServerAPI(NessusEndpoint):

    def status(self):
    '''
    Returns the server status.

    Args:

    Returns:
        dict: The server resource record.

    Examples:
        >>> status = nessus.server.status()
        >>> pprint(status)
    '''  
    return self._api.get('server/status').json()['response']