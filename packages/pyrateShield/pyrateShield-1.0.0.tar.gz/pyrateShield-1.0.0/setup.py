from setuptools import setup, find_packages

APP_NAME = "pyrateshield"

# App version MAJOR.MINOR.PATCH/FIX
APP_VERSION = "1.0.0"
APP_SCRIPT_NAME = "%s.py" % APP_NAME.lower()


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyrateShield',
      python_requires='>=3.8',
      version=APP_VERSION,
      description='Generate radiation-dose maps',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='pyrateShield radiation radiology nuclear medicine',
      url='https://bitbucket.org/MedPhysNL/pyrateShield',
      author='Marcel Segbers, Rob van Rooij',
      author_email='msegbers@gmail.com',
      license='GNU GPLv3',
      packages=find_packages(),

      install_requires=[
          'numpy',
          'scipy',
          'matplotlib',
          'pyqt5',
          'pynrrd',
          'pyyaml',
          'scikit-image',
          'imageio',
          'pandas',
          'psutil',
          'xlsxwriter',
          'xlrd',
          'qtawesome',
          'pyperclip'],

      entry_points={
          'console_scripts': ['pyrateshield=pyrateshield.app:main'],
      },
      include_package_data=True,
      zip_safe=False)
