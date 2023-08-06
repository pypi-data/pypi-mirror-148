from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Package to extend tableauserverclient with further functions'
LONG_DESCRIPTION = 'Includes Class TableauServerConnection and four functions getDataSourcesTableauServer, refreshDataSourceTableauServer, getWorkbooksTableauServer and refreshWorkbookTableauServer'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="tableauserverconnection", 
        version=VERSION,
        author="Edward Oldham",
        author_email="<edward.oldham@me.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['tableauserverclient'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['tableau','refresh data source', 'refresh workbook' ],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)