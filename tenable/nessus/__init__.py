'''

Product: Nessus Professional Version 8

.. autoclass:: TenableNessus

.. automodule:: tenable.nessus.plugins
.. automodule:: tenable.nessus.scans

'''

from tenable.base.v1 import APISession
from tenable.errors import *
from .plugins import PluginAPI
from .scans import ScanAPI
import warnings


class TenableNessus(APISession):

    _supported_version = [8]
    _apikeys = False
    _restricted_paths = ['token']
    _timeout = 300
    _error_codes = {
        400: InvalidInputError,
        403: APIError,
        404: NotFoundError,
        500: ServerError,
    }

    def __init__(self, host, access_key=None, secret_key=None, username=None,
                 password=None, port=8834, ssl_verify=False,
                 adapter=None, scheme='https', retries=None, backoff=None,
                 ua_identity=None, session=None, proxies=None, timeout=None,
                 vendor=None, product=None, build=None):

        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests)
        # understands.
        url = '{}://{}:{}'.format(scheme, host, port)

        # Setting the SSL Verification flag on the object itself so that it's
        # reusable if the user logs out and logs back in.
        self._ssl_verify = ssl_verify

        # Now lets pass the relevent parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        super(TenableNessus, self).__init__(url,
            retries=retries,
            backoff=backoff,
            ua_identity=ua_identity,
            session=session,
            proxies=proxies,
            vendor=vendor,
            product=product,
            build=build,
            timeout=timeout
        )

        # If an adapter for requests was provided, we should pull that in as
        # well.
        if adapter:
            self._session.mount(base, adapter)

        # Now we will attempt to authenticate to the API using any auth settings
        # passed into the constructor.
        self.login(
            access_key=access_key,
            secret_key=secret_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.logout()

    def _build_session(self, session=None):
        super(TenableNessus, self)._build_session(session)
        # As Nessus Professional is generally installed without a certificate chain that
        # we can validate, we will want to turn off verification and the
        # associated warnings unless told to otherwise:
        self._session.verify = self._ssl_verify
        if not self._ssl_verify:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

    def login(self, access_key=None, secret_key=None):
        '''
        Logs the user into Nessus Professional v8

        Args:
            access_key (str, optional): API Access Key
            secret_key (str, optional): API Secret Key

        Returns:
            None

        Examples:

            Using API Keys:

            >>> nessus = TenableNessus('127.0.0.1', port=8443)
            >>> nessus.login(access_key='ACCESSKEY', secret_key='SECRETKEY')
        '''
        if access_key != None and secret_key != None:
            self._session.headers.update({
                'X-APIKeys': 'accessKey={}; secretKey={}'.format(
                    access_key, secret_key)
            })
            self._apikeys = True

    def logout(self):
        '''
        Logs out of Nessus Professional and resets the session.

        Returns:
            None

        Examples:
            >>> nessus.logout()
        '''
        if not self._apikeys:
            resp = self.delete('token')
        self._build_session()
        self._apikeys = False

    @property
    def plugins(self):
        return PluginAPI(self)

    @property
    def scans(self):
        return ScanAPI(self)