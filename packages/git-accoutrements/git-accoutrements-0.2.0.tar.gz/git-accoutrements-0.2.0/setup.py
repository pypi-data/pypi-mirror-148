# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['accoutrements', 'accoutrements.cmd']

package_data = \
{'': ['*']}

install_requires = \
['colored>=1.4.3,<2.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['git-bugfix = accoutrements.cmd.bugfix:main',
                     'git-chore = accoutrements.cmd.chore:main',
                     'git-del = accoutrements.cmd.del:main',
                     'git-ditto = accoutrements.cmd.ditto:main',
                     'git-feature = accoutrements.cmd.feature:main',
                     'git-master = accoutrements.cmd.master:main',
                     'git-rel = accoutrements.cmd.rel:main',
                     'git-tidy = accoutrements.cmd.tidy:main']}

setup_kwargs = {
    'name': 'git-accoutrements',
    'version': '0.2.0',
    'description': 'A collection of tools to help with a git based development workflow',
    'long_description': '# Git Accoutrements\n\nAn opinionated set of git python scripts and that have been developed over time to improve primarily\nGithub flow based workflows.\n\n# Tools\n\n## git master\n\nChecks out the latest copy of the (master|main|trunk) branch of the project and ensures the local\nbranch is up to date.\n\n\n## git (feature|chore|bugfix)\n\nCreates a (feature|chore|bugfix) branch at the current version of the (master|main|trunk) branch.\nUseful in a Github flow based workflow\n\n## git tidy\n\nAttempts to find merged branches / pruned branches in your local repo and will prompt the user to\ndelete them. Quite useful when working on projects that user Github Flow.\n\n## git ditto\n\nA simple replacement for the git clone command, however it will scan up through the filesystem looking \na file called `.git-ditto.toml`. This file can be used to store configuration updates that should be\napplied after the clone.\n\nThis is particularly useful if you want to associate a different git profile (user, email, signingkey)\nfor a particular folder. i.e.\n\n    ~/Code/Work/.git-ditto.toml    # the clones in this folder will have use work profile\n\nAnd\n\n    ~/Code/Home/.git-ditto.toml    # the clones in this folder will have use home profile\n\nExample `.git-ditto.toml`\n\n```toml\n[user]\nname = "<insert name here>"\nemail = "<insert email here>"\nsigningkey = "<insert signing key>"\n```\n\n## git del\n\nDeletes both local and remove copies of a branch\n\n## git rel\n\nCreates a new signed or annotated tag and pushes it up to the upstream repo.\n',
    'author': 'Ed FitzGerald',
    'author_email': 'ejafitzgerald@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ejfitzgerald/git-accoutrements',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
