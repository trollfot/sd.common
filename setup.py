from setuptools import setup, find_packages
from os.path import join

name = 'sd.common'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'Structured Document Common Library',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'plone zope structureddocument',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://tracker.trollfot.org/wiki/StructuredDocument',
      download_url = 'http://pypi.python.org/pypi/sd.common',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['sd'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
          'setuptools',
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
