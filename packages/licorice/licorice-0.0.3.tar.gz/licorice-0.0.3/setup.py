import pathlib, setuptools

VERSION = '0.0.3'

pwd = pathlib.Path(__file__).parent
long_description = (pwd / "README.md").read_text()

setuptools.setup(
        name = 'licorice',
        version = VERSION,
        description = 'Linux Comodular Realtime Interactive Computation Engine',
        author = 'Brain Interfacing Laboratory',
        url = 'http://licorice.stanford.edu',
        long_description = long_description,
        long_description_content_type='text/markdown',
        license = 'GPL2',
        packages = setuptools.find_packages() )
