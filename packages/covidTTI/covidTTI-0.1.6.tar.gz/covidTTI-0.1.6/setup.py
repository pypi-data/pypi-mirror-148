from setuptools import setup

setup(
   name='covidTTI',
   version='0.1.6',
   description='A model estimating the impact of TTI on transmission reduction',
   author='Josie Park',
   author_email='josiepark92@hotmail.co.uk',
   packages=['covidTTI'],
   install_requires=[
      'numpy',
      'PyYaml',
      'scipy'
   ]
)
