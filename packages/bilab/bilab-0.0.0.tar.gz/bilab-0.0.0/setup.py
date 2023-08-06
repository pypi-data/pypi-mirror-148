import pathlib, setuptools

VERSION = '0.0.0'

pwd = pathlib.Path(__file__).parent
long_description = (pwd / "README.md").read_text()

setuptools.setup(
        name = 'bilab',
        version = VERSION,
        description = 'Brain Interfacing Laboratory',
        author = 'Brain Interfacing Laboratory',
        url = 'http://bil.stanford.edu',
        long_description = long_description,
        long_description_content_type='text/markdown',
        license = 'GPL2',
        packages = setuptools.find_packages() )
