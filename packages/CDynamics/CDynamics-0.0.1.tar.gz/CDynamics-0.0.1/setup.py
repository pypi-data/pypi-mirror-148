from setuptools import setup, find_packages
'''
setup(
   name="CDynamics",
   version="0.0.1",
   packages=find_packages(),
   install_requires=['numpy','matplotlib'],
)
'''

VERSION = '0.0.1'
DESCRIPTION = 'Plot Filled-Julia and Julia Sets of Rational Functions'
LONG_DESCRIPTION = 'A package that allows users to plot filled-julia and julia sets of rational holormorhphic self-maps defined on the Riemann sphere'

setup(
    name="CDynamics",
    version=VERSION,
    author="Kanak Dhotre",
    author_email="dhotrekanak@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','matplotlib'],
    keywords=['python', 'complex dynamics', 'julia set', 'filled julia sets'],
)
