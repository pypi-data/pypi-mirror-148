import versioneer
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='drb-xquery',
    packages=find_packages(include=['drb_xquery']),
    description='DRB xquery request',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='GAEL Systems',
    author_email='drb-python@gael.fr',
    url='https://gitlab.com/drb-python/xquery',
    install_requires=REQUIREMENTS,
    setup_requires=['setuptools_scm'],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    use_scm_version=True,
    version=versioneer.get_version(),
    data_files=[('.', ['requirements.txt'])],
    cmdclass=versioneer.get_cmdclass(),
)
