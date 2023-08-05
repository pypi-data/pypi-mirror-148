from setuptools import setup, find_packages


setup(
    name='ucurriculum_student',
    version='0.0.6',
    license='GNU Affero General Public License v3',
    author="Ignacio Palma",
    author_email='ignacio.palma@uc.cl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/IgnacioPalma/UCurriculum-Student',
    keywords='scraper',
    install_requires=[
        'uc_sso',
        'selenium',
        'bs4'
      ],
)