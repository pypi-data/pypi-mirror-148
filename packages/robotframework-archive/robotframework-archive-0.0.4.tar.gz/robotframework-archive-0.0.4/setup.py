from setuptools import find_packages, setup

setup(
      name='robotframework-archive',
      version="0.0.4",
      description='Custom report to display robotframework historical execution records',
      long_description='Robotframework Historic is custom report to display historical execution records using MySQL + Flask',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework historical execution report',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-archive',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'robotframework',
          'config',
          'flask',
          'flask-mysqldb'
      ],
      entry_points={
          'console_scripts': [
              'rfarchive=robotframework_archive.app:main',
              'rfhsparser=robotframework_archive.historic.parserargs:main',
              'rfhsreparser=robotframework_archive.historic.reparserargs:main',
              'rfspparser=robotframework_archive.sp_historic.parserargs:main',
              'rfsfparser=robotframework_archive.sf_historic.parserargs:main',
              'rfarchivesetup=robotframework_archive.setupargs:main',
          ]
      },
)