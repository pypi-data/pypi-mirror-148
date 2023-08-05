# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wavyts']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'sklearn>=0.0,<0.1',
 'tensorflow>=2.8.0,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'wavyts',
    'version': '0.1.3',
    'description': 'Wavy is a library to facilitate time series analysis',
    'long_description': '[![Contributors][contributors-shield]][contributors-url]\n[![Forks][forks-shield]][forks-url]\n[![Stargazers][stars-shield]][stars-url]\n[![Issues][issues-shield]][issues-url]\n[![MIT License][license-shield]][license-url]\n\n\n<!-- PROJECT LOGO -->\n<br />\n<div align="center">\n  <a href="https://github.com/logspace-ai/wavy">\n    <img src="https://github.com/logspace-ai/wavy/blob/main/images/logo.png?raw=true" alt="Logo" width="419" height="235">\n  </a>\n\n  <h3 align="center">Wavy</h3>\n\n  <p align="center">\n    Time Series Done The Right Way\n    <br />\n    <a href="https://github.com/logspace-ai/wavy"><strong>Explore the docs »</strong></a>\n    <br />\n    <br />\n    <a href="https://github.com/logspace-ai/wavy">View Demo</a>\n    ·\n    <a href="https://github.com/logspace-ai/wavy/issues">Report Bug</a>\n    ·\n    <a href="https://github.com/logspace-ai/wavy/issues">Request Feature</a>\n  </p>\n</div>\n\n\n<!-- ABOUT THE PROJECT -->\n## About The Project\n\nWavy is a library to facilitate time series analysis.\n\n\n### Built With\n\n* [Python](https://www.python.org/)\n* [TensorFlow](https://www.tensorflow.org/)\n* [Pandas](https://pandas.pydata.org/)\n* [scikit-learn](https://scikit-learn.org/stable/index.html)\n* [Plotly](https://plotly.com/python/)\n* [NumPy](https://numpy.org/)\n\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nThis is an example of how you may give instructions on setting up your project locally.\nTo get a local copy up and running follow these simple example steps.\n\n\n### Installation\n\n\n```sh\npip install wavyts\n```\n\n\n<!-- USAGE EXAMPLES -->\n## Usage\n\nUse this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.\n\n_For more examples, please refer to the [Documentation](https://example.com)_\n\n\n<!-- ROADMAP -->\n## Roadmap\n\n- [ ] Finish documentation\n- [ ] Migrate models to pytorch\n- [ ] Add Tutorials\n    - [ ] Bovespa\n    - [ ] S&P\n    - [ ] Bitcoin\n\n\nSee the [open issues](https://github.com/logspace-ai/wavy/issues) for a full list of proposed features (and known issues).\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\nIf you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".\nDon\'t forget to give the project a star! Thanks again!\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under the MIT License. See `LICENSE.txt` for more information.\n\n\n<!-- MARKDOWN LINKS & IMAGES -->\n<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->\n[contributors-shield]: https://img.shields.io/github/contributors/logspace-ai/wavy.svg?style=for-the-badge\n[contributors-url]: https://github.com/logspace-ai/wavy/graphs/contributors\n[forks-shield]: https://img.shields.io/github/forks/logspace-ai/wavy.svg?style=for-the-badge\n[forks-url]: https://github.com/logspace-ai/wavy/network/members\n[stars-shield]: https://img.shields.io/github/stars/logspace-ai/wavy.svg?style=for-the-badge\n[stars-url]: https://github.com/logspace-ai/wavy/stargazers\n[issues-shield]: https://img.shields.io/github/issues/logspace-ai/wavy.svg?style=for-the-badge\n[issues-url]: https://github.com/logspace-ai/wavy/issues\n[license-shield]: https://img.shields.io/github/license/logspace-ai/wavy.svg?style=for-the-badge\n[license-url]: https://github.com/logspace-ai/wavy/blob/main/LICENSE.txt\n[product-screenshot]: images/screenshot.png\n',
    'author': 'Ibis Prevedello',
    'author_email': 'ibiscp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/logspace-ai/wavy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
