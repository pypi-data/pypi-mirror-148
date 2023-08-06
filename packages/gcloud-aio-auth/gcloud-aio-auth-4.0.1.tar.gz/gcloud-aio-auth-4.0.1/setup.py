# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcloud', 'gcloud.aio', 'gcloud.aio.auth']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.3.0,<4.0.0',
 'backoff>=1.0.0,<3.0.0',
 'cryptography>=2.0.0,<37.0.0',
 'future>=0.17.0,<0.18.3',
 'pyjwt>=1.5.3,<3.0.0',
 'six>=1.11.0,<2.0.0']

extras_require = \
{':python_full_version < "3.6.2"': ['typing>=3.7.4.1,<4.0.0'],
 ':python_version < "3.6"': ['chardet>=2.0,<4.0'],
 ':python_version >= "3.5" and python_version < "3.6"': ['cffi<1.15.0'],
 ':python_version >= "3.6"': ['chardet>=2.0,<4.1']}

setup_kwargs = {
    'name': 'gcloud-aio-auth',
    'version': '4.0.1',
    'description': 'Python Client for Google Cloud Auth',
    'long_description': '(Asyncio OR Threadsafe) Python Client for Google Cloud Auth\n===========================================================\n\n    This is a shared codebase for ``gcloud-aio-auth`` and ``gcloud-rest-auth``\n\nThis library implements an ``IamClient`` class, which can be used to interact\nwith GCP public keys and URL sign blobs.\n\nIt additionally implements a ``Token`` class, which is used for authorizing\nagainst Google Cloud. The other ``gcloud-aio-*`` package components accept a\n``Token`` instance as an argument; you can define a single token for all of\nthese components or define one for each. Each component corresponds to a given\nGoogle Cloud service and each service requires "`scopes`_".\n\n|pypi| |pythons-aio| |pythons-rest|\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install --upgrade gcloud-{aio,rest}-auth\n\nUsage\n-----\n\n.. code-block:: python\n\n    from gcloud.aio.auth import IamClient\n\n    client = IamClient()\n    pubkeys = await client.list_public_keys()\n\n\n    from gcloud.rest.auth import Token\n\n    token = Token()\n    print(token.get())\n\nAdditionally, the ``Token`` constructor accepts the following optional\narguments:\n\n* ``service_file``: path to a `service account`_, authorized user file, or any\n  other application credentials. Alternatively, you can pass a file-like\n  object, like an ``io.StringIO`` instance, in case your credentials are not\n  stored in a file but in memory. If omitted, will attempt to find one on your\n  path or fallback to generating a token from GCE metadata.\n* ``session``: an ``aiohttp.ClientSession`` instance to be used for all\n  requests. If omitted, a default session will be created. If you use the\n  default session, you may be interested in using ``Token()`` as a context\n  manager (``async with Token(..) as token:``) or explicitly calling the\n  ``Token.close()`` method to ensure the session is cleaned up appropriately.\n* ``scopes``: an optional list of GCP `scopes`_ for which to generate our\n  token. Only valid (and required!) for `service account`_ authentication.\n\nCLI\n~~~\n\nThis project can also be used to help you manually authenticate to test GCP\nroutes, eg. we can list our project\'s uptime checks with a tool such as\n``curl``:\n\n.. code-block:: console\n\n    # using default application credentials\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token().get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\n    # using a service account (make sure to provide a scope!)\n    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service.json\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token(scopes=["\'"https://www.googleapis.com/auth/cloud-platform"\'"]).get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\n    # using legacy account credentials\n    export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/legacy_credentials/EMAIL@DOMAIN.TLD/adc.json\n    curl \\\n      -H "Authorization: Bearer $(python3 -c \'from gcloud.rest.auth import Token; print(Token().get())\')" \\\n      "https://monitoring.googleapis.com/v3/projects/PROJECT_ID/uptimeCheckConfigs"\n\nContributing\n------------\n\nPlease see our `contributing guide`_.\n\n.. _contributing guide: https://github.com/talkiq/gcloud-aio/blob/master/.github/CONTRIBUTING.rst\n.. _scopes: https://developers.google.com/identity/protocols/googlescopes\n.. _service account: https://console.cloud.google.com/iam-admin/serviceaccounts\n.. _smoke test: https://github.com/talkiq/gcloud-aio/blob/master/auth/tests/integration/smoke_test.py\n\n.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-aio-auth.svg?style=flat-square\n    :alt: Latest PyPI Version (gcloud-aio-auth)\n    :target: https://pypi.org/project/gcloud-aio-auth/\n\n.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-aio-auth.svg?style=flat-square&label=python (aio)\n    :alt: Python Version Support (gcloud-aio-auth)\n    :target: https://pypi.org/project/gcloud-aio-auth/\n\n.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-auth.svg?style=flat-square&label=python (rest)\n    :alt: Python Version Support (gcloud-rest-auth)\n    :target: https://pypi.org/project/gcloud-rest-auth/\n',
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/talkiq/gcloud-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
