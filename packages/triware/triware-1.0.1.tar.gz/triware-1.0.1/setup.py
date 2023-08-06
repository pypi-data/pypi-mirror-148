from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()

with open('requirements.txt') as f:
    required = f.readlines()


# specify requirements of your package here
#REQUIREMENTS = ['requests']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

# calling the setup function 
setup(name='triware',
      version='1.0.1',
      description='A script that collects data from sensors and send them to azure blob storage',
      long_description=long_description,
      url='https://github.com/triware/smart-space-management',
      author='Yosri Jendoubi',
      author_email='yosri.jendoubi@esprit.tn',
      license='MIT',
      packages=['rasp'],
      classifiers=CLASSIFIERS,
      install_requires=required,
      keywords='IOT raspberry cloud azure'
      )