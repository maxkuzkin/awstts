#!/usr/bin/env python

import os
from setuptools import setup

PACKAGE_NAME = 'awstts'
DESCRIPTION = 'Amazon Web Services text-to-speech (Polly) helper'


def __find_package_data(folder):
    add_extensions = ['.schema', '.html', '.js', '.css', '.xml', '.jinja', '.bat', '.yaml',
                      '.json', '.png', '.jpg', '.po', '.txt', 'cert.pem', 'key.pem', '.zip',
                      'version']

    file_masks = []
    for subdir, dirs, files in os.walk(folder):
        for f in files:
            filename = f
            name = os.path.join(subdir, f)
            f = f.lower()
            if f in add_extensions:
                file_masks.append(filename)
            elif f.endswith(tuple(add_extensions)):
                path = name[len(folder) + 1:]
                file_mask = os.path.join(os.path.split(path)[0], '*' + os.path.splitext(path)[1])
                if file_mask not in file_masks:
                    file_masks.append(file_mask)

    return file_masks


def get_packages():
    dirs = [PACKAGE_NAME]
    return dirs


def get_package_data():
    data = {}
    data[PACKAGE_NAME] = __find_package_data(PACKAGE_NAME)
    return data


def get_install_requires():
    with open('requirements.txt') as f:
        return f.readlines()


def version():
    _path = os.path.split(os.path.abspath(__file__))[0]
    _file = os.path.join(_path, 'VERSION')
    f = open(_file, 'r')
    ver = f.read()
    f.close()
    return ver.strip()


def odin_version():
    import odintools
    ver = version()
    package_ver, build_num = ver.rsplit('.', 1)
    return odintools.version(package_ver, build_num)


setup(
    name=PACKAGE_NAME,
    version=version(),
    version_getter=odin_version,
    author='Max Kuzkin',
    author_email='maxkuzkin@gmail.com',
    description=DESCRIPTION,
    url='https://github.com/maxkuzkin/awstts',
    license='Apache',
    packages=get_packages(),
    package_data=get_package_data(),
    install_requires=get_install_requires(),
    odintools=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['{0} = {0}.{0}:main'.format(PACKAGE_NAME)]
    }
)
