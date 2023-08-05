# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcware_transpile',
 'qcware_transpile.dialects',
 'qcware_transpile.dialects.braket',
 'qcware_transpile.dialects.pyzx',
 'qcware_transpile.dialects.qiskit',
 'qcware_transpile.dialects.qsharp',
 'qcware_transpile.dialects.quasar',
 'qcware_transpile.translations',
 'qcware_transpile.translations.braket',
 'qcware_transpile.translations.braket.to_quasar',
 'qcware_transpile.translations.pyzx',
 'qcware_transpile.translations.pyzx.to_quasar',
 'qcware_transpile.translations.qiskit',
 'qcware_transpile.translations.qiskit.to_quasar',
 'qcware_transpile.translations.quasar',
 'qcware_transpile.translations.quasar.to_braket',
 'qcware_transpile.translations.quasar.to_pyzx',
 'qcware_transpile.translations.quasar.to_qiskit',
 'qcware_transpile.translations.quasar.to_qsharp',
 'tests',
 'tests.dialects',
 'tests.helpers',
 'tests.matching',
 'tests.performance',
 'tests.serialization',
 'tests.strategies',
 'tests.strategies.braket',
 'tests.strategies.pyzx',
 'tests.strategies.qiskit',
 'tests.strategies.qsharp',
 'tests.strategies.quasar',
 'tests.translations',
 'tests.translations.braket',
 'tests.translations.qiskit',
 'tests.translations.quasar']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'icontract>=2.6.0,<3.0.0',
 'parse>=1.19.0,<2.0.0',
 'pyrsistent>=0.18.0,<0.19.0',
 'toolz>=0.11.2,<0.12.0']

extras_require = \
{'braket': ['amazon-braket-sdk>=1.15.0'],
 'pyzx': ['pyzx>=0.6.4,<0.7.0'],
 'qcware-quasar': ['qcware-quasar>=1.0.6,<2.0.0'],
 'qiskit': ['qiskit-aer>=0.10.0,<0.11.0'],
 'qsharp': ['qsharp>=0.15.2102,<0.16.0']}

setup_kwargs = {
    'name': 'qcware-transpile',
    'version': '0.1.1a21',
    'description': 'A quantum circuit transpilation framework',
    'long_description': None,
    'author': 'Vic Putz',
    'author_email': 'vic.putz@qcware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
