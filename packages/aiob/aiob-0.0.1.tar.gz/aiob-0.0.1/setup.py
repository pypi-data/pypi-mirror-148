# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiob',
 'aiob.api',
 'aiob.api.Destinations.file_markdown',
 'aiob.api.Sources.src_file_markdown',
 'aiob.cli']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.8.1,<4.0.0',
 'colorama>=0.4.4,<0.5.0',
 'dynaconf>=3.1.7,<4.0.0',
 'python-frontmatter>=1.0.0,<2.0.0',
 'shellingham>=1.4.0,<2.0.0',
 'tinydb>=4.7.0,<5.0.0',
 'typer[all]>=0.4.1,<0.5.0']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata>=4.11.3,<5.0.0']}

entry_points = \
{'console_scripts': ['aiob = aiob.cli.main:main']}

setup_kwargs = {
    'name': 'aiob',
    'version': '0.0.1',
    'description': 'All In One Bridge.',
    'long_description': '<div id="top"></div>\n\n<div align="center">\n  <a href="https://github.com/Clouder0/AIOB">\n    <img src="logo.jpg" alt="Logo">\n  </a>\n\n<h3 align="center">AIOB</h3>\n  <p align="center">\n    All In One Bridge for your Datas\n    <br />\n    <a href="https://github.com/Clouder0/AIOB"><strong>Explore the docs »</strong></a>\n  </p>\n</div>\n\n## 📜 TOC\n\n<details>\n  <summary>Table of Contents</summary>\n\n- [🌟 Badges](#🌟-badges)\n- [💡 Introduction](#💡-introduction)\n- [✨ Features](#✨-features)\n- [🎏 Getting Started](#🎏-getting-started)\n- [🗺️ Roadmap](#🗺️-roadmap)\n- [❓ Faq](#❓-faq)\n- [💌 Contributing](#💌-contributing)\n- [🙏 Acknowledgment](#🙏-acknowledgment)\n- [📖 License](#📖-license)\n- [📧 Contact](#📧-contact)\n\n</details>\n\n## 🌟 Badges\n\n[![Test][github-action-test-shield]][github-action-test-url]\n[![Codecov][codecov-shield]][codecov-url]\n[![pre-commit-ci][pre-commit-ci-shield]][pre-commit-ci-url]\n[![pepy-shield]][pepy-url]\n\n[![release-shield]][release-url]\n[![pyversions-shield]][pyversions-url]\n[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![Apache License 2.0][license-shield]][license-url]\n[![CodeFactor-shield]][CodeFactor-url]\n[![code-style-black-shield]][code-style-black-url]\n\n<!-- INTRODUCTION -->\n## 💡 Introduction\n\n**Unfortunately, AIOB is still under initial development and hasn\'t been prepared for users.**  \n**Several embeded sources/destinations will be added until the very first official release. Salient changes might be made to optimize project structures and so on.**  \n**Please wait until version 0.1.0 is published.**  \n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- FEATURES -->\n## ✨ Features\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- GETTING STARTED -->\n## 🎏 Getting Started\n\n<details> <summary>Click Here to Get Started Instantly.</summary>\n\nTODO.\n\n### Installation\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n### Command Line Interface\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n### Configuration\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n### Plugin System\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n</details>\n\n<!-- ROADMAP -->\n## 🗺️ Roadmap\n\nPlease check out our [Github Project](https://github.com/users/Clouder0/projects/2).\n\nSee the [open issues](https://github.com/Clouder0/AIOB/issues) for a full list of proposed features (and known issues).\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- FAQ -->\n## ❓ FAQ\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- CONTRIBUTING -->\n## 💌 Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\nDon\'t forget to see our [Contributing Guideline](https://github.com/Clouder0/AIOB/blob/main/CONTRIBUTING.md) for details.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## 🙏 Acknowledgment\n\nThere are various open source projects that AIOB depends on, without which this tool wouldn\'t exist. Credits to them!\n\n<details> <summary>List</summary>\n\n- [tinydb](https://github.com/msiemens/tinydb), MIT License\n- [Dynaconf](https://github.com/rochacbruno/dynaconf), MIT License\n- [aiofiles](https://github.com/Tinche/aiofiles), Apache License 2.0\n- [python-frontmatter](https://github.com/eyeseast/python-frontmatter), MIT License\n- [typer](https://github.com/tiangolo/typer), MIT License\n- [aiohttp](https://github.com/aio-libs/aiohttp), Apache License 2.0\n- [importlib_metadata](https://github.com/python/importlib_metadata), Apache License 2.0\n\n</details>\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## 📖 License\n\nDistributed under the Apache License 2.0. See `LICENSE` for more information.\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n## 📧 Contact\n\nClouder0\'s email: clouder0@outlook.com\n\nProject Link: [https://github.com/Clouder0/AIOB](https://github.com/Clouder0/AIOB)\n\n<p align="right">(<a href="#top">back to top</a>)</p>\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/Clouder0/AIOB.svg?style=for-the-badge\n[contributors-url]: https://github.com/Clouder0/AIOB/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/Clouder0/AIOB.svg?style=for-the-badge\n[forks-url]: https://github.com/Clouder0/AIOB/network/members\n[stars-shield]: https://img.shields.io/github/stars/Clouder0/AIOB.svg?style=for-the-badge\n[stars-url]: https://github.com/Clouder0/AIOB/stargazers\n[issues-shield]: https://img.shields.io/github/issues/Clouder0/AIOB.svg?style=for-the-badge\n[issues-url]: https://github.com/Clouder0/AIOB/issues\n[license-shield]: https://img.shields.io/github/license/Clouder0/AIOB.svg?style=for-the-badge\n[license-url]: https://github.com/Clouder0/AIOB/blob/main/LICENSE\n[github-action-test-shield]: https://github.com/Clouder0/AIOB/actions/workflows/test.yml/badge.svg?branch=main\n[github-action-test-url]: https://github.com/Clouder0/AIOB/actions/workflows/test.yml\n[codecov-shield]:https://codecov.io/gh/Clouder0/AIOB/branch/main/graph/badge.svg?token=D2XT099AFB\n[codecov-url]: https://codecov.io/gh/Clouder0/AIOB\n[pre-commit-ci-shield]: https://results.pre-commit.ci/badge/github/Clouder0/AIOB/main.svg\n[pre-commit-ci-url]: https://results.pre-commit.ci/latest/github/Clouder0/AIOB/main\n[code-style-black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge\n[code-style-black-url]: https://github.com/psf/black\n[pyversions-shield]: https://img.shields.io/pypi/pyversions/aiob.svg?style=for-the-badge\n[pyversions-url]: https://pypi.org/project/aiob/\n[release-shield]: https://img.shields.io/github/release/Clouder0/AIOB.svg?style=for-the-badge\n[release-url]: https://github.com/Clouder0/AIOB/releases\n[CodeFactor-shield]: https://www.codefactor.io/repository/github/clouder0/aiob/badge/main?style=for-the-badge\n[CodeFactor-url]: https://www.codefactor.io/repository/github/clouder0/aiob/overview/main\n[pepy-shield]: https://static.pepy.tech/personalized-badge/aiob?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads\n[pepy-url]: https://pepy.tech/project/aiob\n',
    'author': 'clouder',
    'author_email': 'clouder0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.github.com/Clouder0/AIOB',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
