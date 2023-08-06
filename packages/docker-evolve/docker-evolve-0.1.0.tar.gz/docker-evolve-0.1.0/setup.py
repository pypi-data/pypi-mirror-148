# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docker_evolve']

package_data = \
{'': ['*']}

install_requires = \
['docker-py>=1.10.6,<2.0.0']

entry_points = \
{'console_scripts': ['docker-evolve = docker_evolve.__main__:main']}

setup_kwargs = {
    'name': 'docker-evolve',
    'version': '0.1.0',
    'description': '',
    'long_description': "# docker-evolve\n\nKeep evolving a container's state to effectively use it as a constant subsystem.\n\n## Usage\n\nStart with a new container:\n\n    $ docker-evolve –-name ubuntu --base-image ubuntu -v $PWD:/host\n\nConnect to the container as usual:\n\n    $ docker exec -it ubuntu bash\n\nAfter making changes that you want to persist but you need to update the container\nconfiguration, for example to expose a port, pass the parameters to `docker-evolve`:\n\n    $ docker-evolve --name ubuntu -v $PWD:/host -p 8090:8090\n\nThis will commit the container's current state and re-create it using the new image\nand the specified arguments. Note how you can now skip the `--base-image` argument\nbecause the container already exists.\n",
    'author': 'Niklas Rosenstein',
    'author_email': 'rosensteinniklas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
