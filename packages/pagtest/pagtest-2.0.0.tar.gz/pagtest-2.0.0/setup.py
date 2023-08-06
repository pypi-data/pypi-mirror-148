from setuptools import setup

setup(
  name='pagtest',
  version='2.0.0',
  description='A print test for PyPI',
  author='wilson',
  author_email='wilson@163.com',
  url='https://www.python.org/',
  license='MIT',
  keywords='a b c',
  project_urls={
    'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
    'Funding': 'https://donate.pypi.org',
    'Source': 'https://github.com/pypa/sampleproject/',
    'Tracker': 'https://github.com/pypa/sampleproject/issues',
  },
  packages=['pagtest'],
  install_requires=['tqdm>=4.63.0', 'twine>=3.8'],
  python_requires='>=3'
  )