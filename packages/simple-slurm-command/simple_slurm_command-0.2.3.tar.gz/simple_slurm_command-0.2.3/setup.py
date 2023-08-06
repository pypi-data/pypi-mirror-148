from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='simple_slurm_command',
    version='0.2.3',
    author='Takuma Yoneda',
    description='A simple Python module to generate Slurm commands built on top of https://github.com/amq92/simple_slurm.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/takuma-yoneda/simple_slurm_command',
    packages=find_packages(),
    package_data={'': ['*.txt']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='GNU Affero General Public License v3',
)
