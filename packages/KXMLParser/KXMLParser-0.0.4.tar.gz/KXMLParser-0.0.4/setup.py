from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='KXMLParser',
    version='0.0.4',
    url='https://github.com/k1k0borba/KXMLParser',
    license='MIT License',
    author='Rodrigo Borba',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='k1k0borba@gmail.com',
    keywords='Xml2Json,XMLParser',
    description=u'Rest Framework Parser xml to json',
    packages=['KXMLParser'],
    install_requires=['xmltodict>=0.12'],)
