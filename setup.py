import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'ijson',
    'pyramid',
    'requests',
    'liblightbase'
]

setup(name='LBBulk',
      version='0.2',
      description='Translator for external keys to fit properly on the lightbase standard',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 2 - Pre-Alpha"
        "Framework :: Pyramid",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English"
        "Programming Language :: Python :: 3",
        "Topic :: Database :: Database Engines/Servers"
        ],
      author='Lightbase',
      author_email='pedro.ricardo@lightbase.com',
      url='',
      keywords='lightbase database translator bulk pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # test_suite='lbbulk',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = lbbulk:main
      [console_scripts]
      initialize_LBBulk_db = lbbulk.scripts.initializedb:main
      """,
      )
