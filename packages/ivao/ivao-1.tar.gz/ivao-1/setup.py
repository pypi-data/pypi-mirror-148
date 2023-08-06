import setuptools



setuptools.setup(
    name="ivao",
    version="1",
    author="Chawalwit Akarajirathanachot",
    author_email="meck22772@gmail.com",
    description="IVAO RestAPI",
    #long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires  = ['requests'],
    license = 'MIT'
)
