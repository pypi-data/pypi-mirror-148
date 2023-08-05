# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ass_tag_parser', 'ass_tag_parser.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ass-tag-parser',
    'version': '2.4.1',
    'description': 'Parse ASS subtitle format tags markup.',
    'long_description': 'ass_tag_parser\n==============\n\n[![Build](https://github.com/bubblesub/ass_tag_parser/actions/workflows/build.yml/badge.svg)](https://github.com/bubblesub/ass_tag_parser/actions/workflows/build.yml)\n\nA Python library for serialization and deserialization of ASS subtitle file\nformat tags markup.\n\nNot to confuse with parsing `.ass` files that can be manipulated with\n[`ass_parser`](https://github.com/bubblesub/ass_parser).\n\n\n**Example**:\n\n```python3\nfrom ass_tag_parser import parse_ass\n\n\nresult = parse_ass(\n    r"{\\an5\\pos(175,460)\\fnUtopia with Oldstyle figures\\fs90\\bord0\\blur3"\n    r"\\1c&H131313&\\t(0,1000,2,\\1c&H131340&)\\t(1000,2000,\\1c&H1015B2&"\n    r"\\blur1.4)}Attack No. 1{NOTE:アタックNo.1}"\n)\nprint(result)\nprint(result[2].meta)\n```\n\n**Result**:\n\n```python3 console\n[\n    AssTagListOpening(),\n    AssTagAlignment(alignment=5, legacy=False),\n    AssTagPosition(x=175.0, y=460.0),\n    AssTagFontName(name="Utopia with Oldstyle figures"),\n    AssTagFontSize(size=90.0),\n    AssTagBorder(size=0.0),\n    AssTagBlurEdgesGauss(weight=3.0),\n    AssTagColor(red=19, green=19, blue=19, target=1, short=False),\n    AssTagAnimation(\n        tags=[AssTagColor(red=64, green=19, blue=19, target=1, short=False)],\n        time1=0.0,\n        time2=1000.0,\n        acceleration=2.0,\n    ),\n    AssTagAnimation(\n        tags=[\n            AssTagColor(red=178, green=21, blue=16, target=1, short=False),\n            AssTagBlurEdgesGauss(weight=1.4),\n        ],\n        time1=1000.0,\n        time2=2000.0,\n        acceleration=None,\n    ),\n    AssTagListEnding(),\n    AssText(text="Attack No. 1"),\n    AssTagListOpening(),\n    AssTagComment(text="NOTE:アタックNo.1"),\n    AssTagListEnding(),\n]\nMeta(start=5, end=18, text="\\\\pos(175,460)")\n```\n\nStarting from version 2.2, drawing commands are parsed automatically.\n\n---\n\n### Serializing the tree back\n\nASS tree: `compose_ass`. Note that you don\'t need to supply `AssTagListOpening`\nnor `AssTagListEnding` tags in the input item list – this function inserts them\nautomatically.\n\nDraw commands: `compose_draw_commands`.\n\n# Contributing\n\n```sh\n# Clone the repository:\ngit clone https://github.com/bubblesub/ass_tag_parser.git\ncd ass_tag_parser\n\n# Install to a local venv:\npoetry install\n\n# Install pre-commit hooks:\npoetry run pre-commit install\n\n# Enter the venv:\npoetry shell\n```\n\nThis project uses [poetry](https://python-poetry.org/) for packaging,\ninstall instructions at [poetry#installation](https://python-poetry.org/docs/#installation)\n',
    'author': 'Marcin Kurczewski',
    'author_email': 'dash@wind.garden',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bubblesub/ass_tag_parser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
