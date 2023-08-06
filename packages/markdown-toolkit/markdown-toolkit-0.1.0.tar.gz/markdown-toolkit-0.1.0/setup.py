# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['markdown_toolkit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'markdown-toolkit',
    'version': '0.1.0',
    'description': 'Utility package for programmatically creating markdown documents',
    'long_description': '# Markdown Toolkit\n> **INFO**: _This readme is dynamically generated via `generate_readme.py`._\n\n\nA python library for creating markdown.\n\n\nThis library heavily utilises context managers\n        to encapsulate logical blocks in the markdown. Primarily this is used\n        to keep track of the heading levels, so nested `Heading` context\n        managers will be aware of the parent header level.\n\n\n## Example Usage\n\n\n```python\nfrom markdown_toolkit import MarkdownBuilder, Heading\n\nwith MarkdownBuilder() as doc:\n    with Heading(doc, "Markdown Toolkit"):\n        doc.paragraph("Example Paragraph.")\n        with Heading(doc, "Nested Header"):\n            doc.paragraph("Nested.")\n\nwith open("example.md", "w", encoding="UTF-8") as file:\n    doc.write(file)\n```\n\n',
    'author': 'Daniel Loader',
    'author_email': 'hello@danielloader.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/danielloader/markdown-toolkit/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
