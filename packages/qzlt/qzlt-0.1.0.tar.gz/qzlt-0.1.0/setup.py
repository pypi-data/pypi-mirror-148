# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qzlt']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['quiz = qzlt.main:app', 'test = scripts:run_tests']}

setup_kwargs = {
    'name': 'qzlt',
    'version': '0.1.0',
    'description': 'A Quizlet clone for the command line',
    'long_description': '<div id="top"></div>\n\n\n\n<br />\n<div align="center">\n  <h3 align="center">qzlt</h3>\n  <p align="center">\n    A <a href="https://quizlet.com">Quizlet</a> clone for the command line.\n  </p>\n  <img src="docs/screenshot.gif" alt="Screenshot" width="580" />\n</div>\n\n\n\n## Built With\n\n* [Python](https://www.python.org/)\n* [Typer](https://typer.tiangolo.com/)\n* [Poetry](https://python-poetry.org/)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n## Installation\n\n#### PyPI\n\n```\npip install qzlt\n```\n\n#### From source\n\nWith [Poetry](https://python-poetry.org) installed, run\n```\ngit clone https://github.com/calvincheng/qzlt.git\ncd qzlt\npoetry shell\npoetry install\n```\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n## Usage\n\n### Quick start\n\nLet\'s create a new set to start learning some common Chinese vocabulary. Run\n```\nquiz sets create\n```\n```\nTitle: chinese\nDescription: Common expressions in Chinese\n```\nand follow the prompts to give your set a title and a description.\n\nYou can see that the newly created set exists by listing all sets via\n```\nquiz sets list\n```\n```\nTITLE               DESCRIPTION\nchinese             Common expressions in Chinese\n```\n\nBy default, new sets are empty when created. Let\'s change that by adding some cards. Run\n```\nquiz set add chinese\n```\n\nYou\'ll be prompted to start giving your card a term and a definition.\n```\nTerm: 你好\nDefinition: Hello\nCard added\n```\n\nAdd as many cards as you want. When you\'re done, press `ctrl-C` to exit.\n\nTo see all the cards you\'ve just added, run\n```\nquiz set list chinese\n```\n```\n      TERM         DEFINITION\n[0]   你好          Hello\n[1]   再見          Goodbye\n[2]   開心          Happy\n[3]   傷心          Sad\n[4]   蘋果          Apple\n[5]   香蕉          Banana\n```\n\nYou\'re all set! To study your new set, run\n```\nquiz study chinese\n```\n\nTo see all the study modes available, run\n```\nquiz study --help\n```\n\n### Commands\n\n```\nUsage: quiz [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n  --help                Show this message and exit.\n\nCommands:\n  set    Manage an individual set\n  sets   Manage all sets\n  study  Begin a study session\n```\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n## Roadmap\n\n- [ ] Import from Anki\n- [ ] Collect and display statistics (review heatmap, streaks, etc.)\n- [ ] Add config file to customise experience (e.g. shuffle by default)\n- [ ] Smarter corrections (e.g. allow answers from either grammatical gender: professeur•e)\n- [ ] Markdown support for cards\n- [ ] Incorporate TTS\n- [ ] Resume interrupted sessions\n\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n## License\n\nDistributed under the [MIT License](https://github.com/calvincheng/qzlt/blob/master/LICENSE).\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n\n\n## Contact\n\nCalvin Cheng - calvin.cc.cheng@gmail.com\n\nProject Link: [https://github.com/calvincheng/qzlt](https://github.com/calvincheng/qzlt)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n',
    'author': 'Calvin Cheng',
    'author_email': 'calvin.cc.cheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
