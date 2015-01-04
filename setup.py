import os
import sys
from setuptools import setup, find_packages
from pkg_resources import require, DistributionNotFound


def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

readme_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'README.rst'))

try:
    long_description = open(readme_file).read()
except IOError as err:
    sys.stderr.write("[ERROR] Cannot find file specified as long_description (%s)\n" % readme_file)
    sys.exit(1)

extra_kwargs = {'tests_require': ['mock>1.0']}

ydcommon = __import__('ydcommon')

requirements = local_open('requirements.txt')
required_to_install = []
for dist in requirements.readlines():
    dist = dist.strip()
    try:
        require(dist)
    except DistributionNotFound:
        required_to_install.append(dist)

setup(
    name='ydcommon',
    version=ydcommon.get_version(),
    url='https://github.com/ArabellaTech/ydcommon',
    author='Arabella',
    author_email='team@arabel.la',
    description=ydcommon.__doc__,
    long_description=long_description,
    zip_safe=False,
    install_requires=required_to_install,
    packages=find_packages(),
    license='MIT',
    scripts=[],
    test_suite="test_project.runtests.runtests",
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    **extra_kwargs
)
