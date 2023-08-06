from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='p1-oracles-client',
    version='0.1.0.dev0',
    description='Cliente web para o p1-oracles-server',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/daltonserey/p1-oracles-client',
    author='Dalton Serey',
    author_email='daltonserey@gmail.com',
    maintainer='Dalton Serey',
    maintainer_email='daltonserey@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>3.6',
    install_requires=[
        'p1ufcg>=0.2.4'
    ],
    entry_points = {
        'console_scripts': [
            'p1-oracles-check=oracles_client:check',
        ]
    },
)
