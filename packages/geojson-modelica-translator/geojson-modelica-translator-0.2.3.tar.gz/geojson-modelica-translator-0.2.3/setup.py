# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geojson_modelica_translator',
 'geojson_modelica_translator.geojson',
 'geojson_modelica_translator.model_connectors',
 'geojson_modelica_translator.model_connectors.couplings',
 'geojson_modelica_translator.model_connectors.districts',
 'geojson_modelica_translator.model_connectors.energy_transfer_systems',
 'geojson_modelica_translator.model_connectors.load_connectors',
 'geojson_modelica_translator.model_connectors.networks',
 'geojson_modelica_translator.model_connectors.plants',
 'geojson_modelica_translator.modelica',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.AC.ThreePhasesBalanced.Conversion',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.AC.ThreePhasesBalanced.Lines',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.AC.ThreePhasesBalanced.Loads',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.AC.ThreePhasesBalanced.Sources',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.AC.ThreePhasesBalanced.Storage',
 'geojson_modelica_translator.modelica.GMT_Lib.Electrical.DC.Loads',
 'geojson_modelica_translator.modelica.lib',
 'geojson_modelica_translator.modelica.lib.runner',
 'geojson_modelica_translator.system_parameters',
 'management']

package_data = \
{'': ['*'],
 'geojson_modelica_translator.geojson': ['data/schemas/*'],
 'geojson_modelica_translator.model_connectors.couplings': ['templates/CoolingIndirect_Network2Pipe/*',
                                                            'templates/CoolingIndirect_NetworkChilledWaterStub/*',
                                                            'templates/HeatingIndirect_Network2Pipe/*',
                                                            'templates/HeatingIndirect_NetworkHeatedWaterStub/*',
                                                            'templates/Network2Pipe_CoolingPlant/*',
                                                            'templates/Network2Pipe_HeatingPlant/*',
                                                            'templates/NetworkChilledWaterStub_CoolingPlant/*',
                                                            'templates/NetworkHeatedWaterStub_HeatingPlant/*',
                                                            'templates/Spawn_CoolingIndirect/*',
                                                            'templates/Spawn_EtsColdWaterStub/*',
                                                            'templates/Spawn_EtsHotWaterStub/*',
                                                            'templates/Spawn_HeatingIndirect/*',
                                                            'templates/Teaser_CoolingIndirect/*',
                                                            'templates/Teaser_EtsColdWaterStub/*',
                                                            'templates/Teaser_EtsHotWaterStub/*',
                                                            'templates/Teaser_HeatingIndirect/*',
                                                            'templates/TimeSeriesMFT_CoolingIndirect/*',
                                                            'templates/TimeSeriesMFT_HeatingIndirect/*',
                                                            'templates/TimeSeries_CoolingIndirect/*',
                                                            'templates/TimeSeries_EtsColdWaterStub/*',
                                                            'templates/TimeSeries_EtsHotWaterStub/*',
                                                            'templates/TimeSeries_HeatingIndirect/*'],
 'geojson_modelica_translator.model_connectors.districts': ['templates/*'],
 'geojson_modelica_translator.model_connectors.energy_transfer_systems': ['templates/*'],
 'geojson_modelica_translator.model_connectors.load_connectors': ['templates/*'],
 'geojson_modelica_translator.model_connectors.networks': ['templates/*'],
 'geojson_modelica_translator.model_connectors.plants': ['templates/*'],
 'geojson_modelica_translator.modelica': ['GMT_Lib/DHC/Components/Plants/Cooling/*',
                                          'GMT_Lib/Electrical/Examples/*',
                                          'model_connectors/templates/*',
                                          'templates/*'],
 'management': ['data/*']}

install_requires = \
['BuildingsPy==2.1.0',
 'click==7.1.2',
 'geojson==2.5.0',
 'jinja2==3.1.1',
 'jsonpath-ng==1.5.2',
 'jsonschema==3.2.0',
 'modelica-builder>=0.2.1,<0.3.0',
 'pandas==1.3.5',
 'requests==2.25.1',
 'teaser==0.7.5']

entry_points = \
{'console_scripts': ['check_sys_params = '
                     'management.check_sys_params:check_sys_params',
                     'format_modelica_files = '
                     'management.format_modelica_files:fmt_modelica_files',
                     'uo_des = management.uo_des:cli',
                     'update_licenses = '
                     'management.update_licenses:update_licenses',
                     'update_schemas = '
                     'management.update_schemas:update_schemas']}

setup_kwargs = {
    'name': 'geojson-modelica-translator',
    'version': '0.2.3',
    'description': 'Package for converting GeoJSON to Modelica models for Urban Scale Analyses.',
    'long_description': 'GeoJSON Modelica Translator (GMT)\n---------------------------------\n\n.. image:: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml/badge.svg?branch=develop\n    :target: https://github.com/urbanopt/geojson-modelica-translator/actions/workflows/ci.yml\n\n.. image:: https://coveralls.io/repos/github/urbanopt/geojson-modelica-translator/badge.svg?branch=develop\n    :target: https://coveralls.io/github/urbanopt/geojson-modelica-translator?branch=develop\n\n.. image:: https://badge.fury.io/py/geojson-modelica-translator.svg\n    :target: https://badge.fury.io/py/geojson-modelica-translator\n\nDescription\n-----------\n\nThe GeoJSON Modelica Translator (GMT) is a one-way trip from GeoJSON in combination with a well-defined instance of the system parameters schema to a Modelica package with multiple buildings loads, energy transfer stations, distribution networks, and central plants. The project will eventually allow multiple paths to build up different district heating and cooling system topologies; however, the initial implementation is limited to 1GDH and 4GDHC.\n\nThe project is motivated by the need to easily evaluate district energy systems. The goal is to eventually cover the various generations of heating and cooling systems as shown in the figure below. The need to move towards 5GDHC systems results in higher efficiencies and greater access to additional waste-heat sources.\n\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-generations.png\n\nGetting Started\n---------------\n\nIt is possible to test the GeoJSON to Modelica Translator (GMT) by simpling installing the Python package and running the\ncommand line interface (CLI) with results from and URBANopt SDK set of results. However, to fully leverage the\nfunctionality of this package (e.g., running simulations), then you must also install the Modelica Buildings\nlibrary (MBL) and Docker. Instructions for installing and configuring the MBL and Docker are available\n`here <docs/getting_started.rst>`_.\n\nTo simply scaffold out a Modelica package that can be inspected in a Modelica environment (e.g., Dymola) then\nrun the following code below up to the point of run-model. The example generates a complete 4th Generation District\nHeating and Cooling (4GDHC) system with time series loads that were generated from the URBANopt SDK using\nOpenStudio/EnergyPlus simulations.\n\n.. code-block:: bash\n\n    pip install geojson-modelica-translator\n\n    # from the simulation results within a checkout of this repository\n    # in the ./tests/management/data/sdk_project_scraps path.\n\n    # generate the system parameter from the results of the URBANopt SDK and OpenStudio Simulations\n    uo_des build-sys-param sys_param.json baseline_scenario.csv example_project.json\n\n    # create the modelica package (requires installation of the MBL)\n    uo_des create-model sys_param.json example_project.json model_from_sdk\n\n    # test running the new Modelica package (requires installation of Docker)\n    uo_des run-model model_from_sdk\n\nMore example projects are available in an accompanying\n`example repository <https://github.com/urbanopt/geojson-modelica-translator-examples>`_.\n\nArchitecture Overview\n---------------------\n\nThe GMT is designed to enable "easy" swapping of building loads, district systems, and newtork topologies. Some\nof these functionalities are more developed than others, for instance swapping building loads between Spawn and\nRC models (using TEASER) is fleshed out; however, swapping between a first and fifth generation heating system has\nyet to be fully implemented.\n\nThe diagram below is meant to illustrate the future proposed interconnectivity and functionality of the\nGMT project.\n\n.. image:: https://raw.githubusercontent.com/urbanopt/geojson-modelica-translator/develop/docs/images/des-connections.png\n\nAs shown in the image, there are multiple building loads that can be deployed with the GMT and are described in the `Building Load Models`_ section below. These models, and the associated design parameters, are required to create a fully runnable Modelica model. The GMT leverages two file formats for generating the Modelica project and are the GeoJSON feature file and a System Parameter JSON file. See the more `comprehensive\ndocumentation on the GMT <https://docs.urbanopt.net/geojson-modelica-translator/>`_ or the `documentation on\nURBANopt SDK  <https://docs.urbanopt.net/>`_.\n\nBuilding Load Models\n++++++++++++++++++++\n\nThe building loads can be defined multiple ways depending on the fidelity of the required models. Each of the building load models are easily replaced using configuration settings within the System Parameters file. The 4 different building load models include:\n\n#. Time Series in Watts: This building load is the total heating, cooling, and domestic hot water loads represented in a CSV type file (MOS file). The units are Watts and should be reported at an hour interval; however, finer resolution is possible. The load is defined as the load seen by the ETS.\n#. Time Series as mass flow rate and delta temperature: This building load is similar to the other Time Series model but uses the load as seen by the ETS in the form of mass flow rate and delta temperature. The file format is similar to the other Time Series model but the columns are mass flow rate and delta temperature for heating and cooling separately.\n#. RC Model: This model leverages the TEASER framework to generate an RC model with the correct coefficients based on high level parameters that are extracted from the GeoJSON file including building area and building type.\n#. Spawn of EnergyPlus: This model uses EnergyPlus models to represent the thermal zone heat balance portion of the models while using Modelica for the remaining components. Spawn of EnergyPlus is still under development and currently only works on Linux-based systems.\n',
    'author': 'URBANopt DES Team',
    'author_email': 'nicholas.long@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.urbanopt.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
