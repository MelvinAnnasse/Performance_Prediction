from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(filepath:str)->List[str]:
    '''
    Returns the list of requirements in a list
    '''
    requirements = []
    with open(filepath) as fileobj:
        requirements = fileobj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='Performance_prediction Project',
    version='0.0.1',
    author='Melvin_Annasse',
    author_email='learning.melvinannasse@gmail.com',
    packages=find_packages(),
    requires=get_requirements('requirements.txt')

)