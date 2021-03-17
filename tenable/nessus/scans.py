'''
scans
=====

The following methods allow for interaction into the Nessus Professional

Methods available on ``nessus.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScanAPI

    .. automethod:: list
    .. automethod:: export_scan
'''

from .base import NessusEndpoint
import time

class ScanAPI(NessusEndpoint):

    def list(self):
        '''
        Retrieves the list of scans.

        Args:

        Returns:
            :obj:`list`:
                A list of scan resources.

        Examples:
            >>> for scan in nessus.scans.list():
            ...     pprint(scan)
        '''
        return self._api.get('scans').json()['scans']

    def export_scan(self, id: int, fobj=None, export_format="nessus"):
        '''
        Downloads scan results to file

        Args:
            :id:`int`:
                ID of the scan result
            :fobj:`BytesIO`:
                File-like object to store results.
            :export_format:`string`:
                Format of the scan result.

        Returns:
            :obj:`BytesIO`:
                Scan results in a file-like object.
        '''
        # Request download for scan id
        resp = self._api.post(f'scans/{id}/export',
                                  json={'format': export_format}).json()
        token = resp['token']
        file_id = resp['file']

        # Check status of requested download
        while True:
            status = self._api.get('scans/{}/export/{}/status'.format(
                self._check('id', id, int), file_id)).json()['status']
            if status == 'ready':
                break
            time.sleep(1)

        # if no file-like object was passed, then we will instantiate a BytesIO
        # object to push the file into.
        if not fobj:
            fobj = BytesIO()

        # Download scan
        resp = self._api.get('scans/{}/export/{}/download'.format(
            self._check('id', id, int), file_id), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj