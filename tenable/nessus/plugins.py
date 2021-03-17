'''
plugins
=======

The following methods allow for interaction with the Nessus Professional

Methods available on ``nessus.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginAPI

    .. automethod:: families
    .. automethod:: familiy_details
    .. automethod:: details
'''

from .base import NessusEndpoint

class PluginAPI(NessusEndpoint):

    def families(self) -> dict:
        '''
        Returns the list of plugin families.

        Args:

        Returns:
            dict: List of families.

        Examples:
            >>> families = nessus.plugins.families()
            >>> pprint(families)
        '''
        return self._api.get('plugins/families').json()

    def families_details(self, id: int) -> dict:
        '''
        Returns the list of plugins in a family.

        Args:

        Returns:
            dict: List of all plugins including id and name.

        Examples:
            >>> details = nessus.plugins.families_details(27)
            >>> pprint(details)
        '''
        return self._api.get('plugins/families/{}'.format(
            self._check('id', id, int))).json()

    def details(self, id: int) -> dict:
        '''
        Returns the details for a specific plugin.

        Args:
            id (int): The identifier for the plugin.

        Returns:
            dict: The plugin resource record.

        Examples:
            >>> plugin = nessus.plugins.details(19506)
            >>> pprint(plugin)
        '''
        return self._api.get('plugins/plugin/{}'.format(
            self._check('id', id, int))).json()
