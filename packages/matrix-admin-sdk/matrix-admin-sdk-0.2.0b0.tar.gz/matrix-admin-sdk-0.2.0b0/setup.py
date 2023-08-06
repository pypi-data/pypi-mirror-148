# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_admin_sdk',
 'matrix_admin_sdk.endpoints',
 'matrix_admin_sdk.endpoints.v1',
 'matrix_admin_sdk.endpoints.v2',
 'matrix_admin_sdk.models',
 'matrix_admin_sdk.models.v1',
 'matrix_admin_sdk.models.v2']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'matrix-admin-sdk',
    'version': '0.2.0b0',
    'description': 'Async wrapper for matrix.org admin API',
    'long_description': '# Matrix Admin Sdk\n\n[![PyPI version](https://badge.fury.io/py/matrix-admin-sdk.svg)](https://badge.fury.io/py/matrix-admin-sdk)\n\nAsync wrapper for matrix.org admin API\n\n\n## Installation\n```shell\npip install matrix-admin-sdk\n```\n\n## Usage\nDocumentations [here](https://dmitriiweb.github.io/matrix-admin-sdk/)\n\n### Quick Start\n```python\nimport asyncio\n\nimport httpx\n\nfrom matrix_admin_sdk import MatrixAdminClient\nfrom matrix_admin_sdk.endpoints.v1 import EditRoomMembership\n\n\nasync def main():\n    admin_key = "admin_key"\n    http_client = httpx.AsyncClient()\n    server_url = "https://matrix.server.com"\n\n    admin_client = MatrixAdminClient(http_client, admin_key, server_url)\n\n    api = EditRoomMembership(admin_client)\n    res = await api.join_user_to_room("room_id", "user_id")\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```',
    'author': 'Dmitrii Kurlov',
    'author_email': 'dmitriik@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmitriiweb/matrix-admin-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
