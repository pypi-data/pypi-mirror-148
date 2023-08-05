from setuptools import setup, find_packages

# The text of the README file
with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name='cfcapi',
    version='1.0.1',
    license='MIT',
    author="César J. Lockhart de la Rosa",
    author_email='lockhart@imec.be',
    description="API for the Caonabo Fluidic Controller (CFC)",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    url='https://github.imec.be/dna-storage/cfcapi',
    keywords='fluidic controller, api, caonabo',
    install_requires=['pyserial'],

)