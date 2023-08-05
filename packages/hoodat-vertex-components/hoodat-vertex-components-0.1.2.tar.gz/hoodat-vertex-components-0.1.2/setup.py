# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoodat_vertex_components',
 'hoodat_vertex_components.components',
 'hoodat_vertex_components.components.add_py',
 'hoodat_vertex_components.components.haar_from_frames',
 'hoodat_vertex_components.components.make_cascade_file',
 'hoodat_vertex_components.components.make_cascade_file.tests',
 'hoodat_vertex_components.components.video_to_frames']

package_data = \
{'': ['*']}

install_requires = \
['hoodat-utils>=0.0.5,<0.0.6', 'kfp>=1.8.12,<2.0.0']

setup_kwargs = {
    'name': 'hoodat-vertex-components',
    'version': '0.1.2',
    'description': 'Re-usable kfp components for hoodat',
    'long_description': '# Hoodat Pipeline Components\n\nThis repository provides an SDK and a set of components that perform\ntasks in hoodat.\n\nIt is modelled after this repository of shared components for GCP:\nhttps://github.com/kubeflow/pipelines/tree/google-cloud-pipeline-components-1.0.1/components/google-cloud\n\n## To publish package to pypi:\n\n1. Update the version in `pyproject.toml`\n\n2. Run `poetry publish`:\n```\npoetry publish --build\n```\n',
    'author': 'Eugene Brown',
    'author_email': 'efbbrown@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
