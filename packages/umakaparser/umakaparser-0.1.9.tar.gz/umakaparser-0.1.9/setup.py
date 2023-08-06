# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umakaparser', 'umakaparser.scripts', 'umakaparser.scripts.services']

package_data = \
{'': ['*'], 'umakaparser': ['locales/*']}

install_requires = \
['click>=8.0,<9.0',
 'isodate>=0.6.0,<0.7.0',
 'pyparsing>=3.0,<4.0',
 'python-i18n>=0.3.9,<0.4.0',
 'rdflib>=6.0.0,<7.0.0',
 'tqdm>=4.52.0,<5.0.0']

entry_points = \
{'console_scripts': ['umakaparser = umakaparser.services:cmd']}

setup_kwargs = {
    'name': 'umakaparser',
    'version': '0.1.9',
    'description': '',
    'long_description': '# UmakaParser\n\nThis tool is to make a JSON for [Umaka Viewer](https://umaka-viewer.dbcls.jp/).\n\u200b\nFirst, you need to prepare a metadata file in the [SPARQL Builder Meatadata (SBM)](http://www.sparqlbuilder.org/doc/sbm_2015sep/) format.\nIf you want to get such a metadata file, [TripleDataProfiler](https://bitbucket.org/yayamamo/tripledataprofiler/src/master/) can generate it for a SPARQL endpoint.\n\u200b\nThen, if you have ontology files for the target endpoint or RDF dataset, you need to make asset files by this tool as follows.\n\u200b\n`umakaparser --build-index [--dist <Path to put an asset file>] <ontology files in Turtle>`\n\u200b\nIf you have ontology files only in RDF/XML, this tool converts them into those in Turtle as follows.\n\u200b\n`umakaparser --convert <files in RDF/XML>`\n\u200b\nFinally, this tool generates a JSON file that can be accepted by [Umaka Viewer](https://umaka-viewer.dbcls.jp/) as follows.\n\u200b\n`umakaparser --build [--a <Path to asset files>|--d <Path to put a generated JSON file>] <an SBM file>`\n\u200b\nThe JSON file structure is [here](https://github.com/dbcls/umakaparser/wiki/Data-specification).\n',
    'author': 'DBCLS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://umaka-viewer.dbcls.jp/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
