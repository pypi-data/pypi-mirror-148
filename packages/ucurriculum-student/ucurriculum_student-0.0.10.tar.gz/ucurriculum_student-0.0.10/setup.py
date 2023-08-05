from setuptools import setup

setup(
    name='ucurriculum_student',
    version='0.0.10',
    license='GNU Affero General Public License v3',
    author="Ignacio Palma",
    author_email='ignacio.palma@uc.cl',
    packages=['UCurriculum-Student'],
    url='https://github.com/IgnacioPalma/UCurriculum-Student',
    keywords='scraper',
    install_requires=[
        'uc_sso',
        'selenium',
        'bs4'
      ],
)