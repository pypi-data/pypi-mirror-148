from setuptools import setup
from pathlib import Path

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name='pytest-tst',
    version='0.1.3',
    description='Customize pytest options, output and exit code to make it compatible with tst',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/daltonserey/pytest-tst',
    author='Dalton Serey',
    author_email='daltonserey@gmail.com',
    maintainer='Dalton Serey',
    maintainer_email='daltonserey@gmail.com',
    license='MIT',
    py_modules=['pytest_tst'],
    python_requires='>3.6',
    install_requires=[
        'pytest>=5.0.0',
        'tst>=0.15.1'
    ],
    entry_points={
        'pytest11': [
            'tst = pytest_tst',
        ],
    },
)
