# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simsi_transfer', 'simsi_transfer.utils']

package_data = \
{'': ['*'],
 'simsi_transfer.utils': ['ThermoRawFileParser/*',
                          'maracluster/linux64/*',
                          'maracluster/win64/*']}

install_requires = \
['lxml>=4.8.0,<5.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pyteomics>=4.5.3,<5.0.0']

setup_kwargs = {
    'name': 'simsi-transfer',
    'version': '0.3.0',
    'description': 'Software-assisted reduction of missing values in phosphoproteomics and proteomics isobaric labeling data using MS2 spectrum clustering',
    'long_description': '# SIMSI-Transfer\n\nTransferring identifications using MS2 spectrum clustering with MaxQuant search results.\n\nHamood, F., Bayer, F. P., Wilhelm, M., Kuster, B., & The, M. (2022). _[SIMSI-Transfer: Software-assisted reduction of missing values in phosphoproteomic and proteomic isobaric labeling data using tandem mass spectrum clustering.](https://www.sciencedirect.com/science/article/pii/S1535947622000469)_ Molecular & Cellular Proteomics, 100238.\n\n## Test dataset\n\nFor testing SIMSI-Transfer after installation, we recommend downloading the TMT11 MS2 raw files from this publication:\nThompson, A., Wölmer, N., Koncarevic, S., Selzer, S. et al., _[TMTpro: Design, Synthesis, and Initial Evaluation of a Proline-Based Isobaric 16-Plex Tandem Mass Tag Reagent Set.](https://pubs.acs.org/doi/abs/10.1021/acs.analchem.9b04474)_ Analytical Chemistry 2019, 91, 15941–15950. doi:10.1021/acs.analchem.9b04474\n\nPRIDE link: https://www.ebi.ac.uk/pride/archive/projects/PXD014750\n\nRaw files for TMT-MS2:\n- 19070-001.raw\n- 19070-002.raw\n- 19070-003.raw\n- 19070-006.raw\n- 19070-007.raw\n- 19070-008.raw\n\nThe MaxQuant results needed as input to SIMSI-Transfer can be downloaded from Zenodo: \n- [10.5281/zenodo.6365902](https://zenodo.org/record/6365902)\n\nFor reference, the original SIMSI-Transfer results (v0.1.0) for this dataset can also be downloaded from Zenodo:\n- [10.5281/zenodo.6365638](https://zenodo.org/record/6365638)\n\n## Running SIMSI-Transfer using the GUI\n\nOn Windows, you can download the `SIMSI-Transfer_GUI_windows.zip` from the latest release, unzip it and open `SIMSI-Transfer.exe` to start the GUI (no installation necessary).\n\nAlternatively, on all platforms, first install SIMSI-Transfer as explained below. Then install `PyQt5` (`pip install PyQt5`) and run:\n\n```shell\npython gui.py\n```\n\n## Running SIMSI-Transfer from the command line\n\nFirst install SIMSI-Transfer as explained below, then run SIMSI-Tranfer:\n\n```shell\npython -m simsi_transfer --mq_txt_folder </path/to/txt/folder> --raw_folder </path/to/raw/folder> --output_folder </path/to/output/folder>\n```\n\n## Installation\n\nSIMSI-Tranfer is available on PyPI and can be installed with `pip`:\n\n```shell\npip install simsi-transfer\n```\n\nAlternatively, you can install directly from this repository:\n\n```shell\ngit clone https://github.com/kusterlab/SIMSI-Transfer.git\npip install .\n```\n',
    'author': 'Firas Hamood',
    'author_email': 'firas.hamood@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kusterlab/SIMSI-Transfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
