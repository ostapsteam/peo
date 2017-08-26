import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='peo',
    version='0.19',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='rest',
    long_description=README,
    url='',
    author='Alex Korotkov',
    author_email='alexkorotkovru@yandex.ru',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['flask', 'sqlalchemy', 'mysqlclient', 'gunicorn', 'alembic'],
    entry_points={
        'console_scripts': [
            'peo-server = peo.app:main',
            'peo-database-manage = peo.manage:main',
        ]
    }
)