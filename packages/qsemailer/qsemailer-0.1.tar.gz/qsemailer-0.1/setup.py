from setuptools import setup, find_packages

setup(
    name='qsemailer',
    version='0.1',
    license='MIT',
    author="Fabian Rücker",
    author_email='rueckerfab@aol.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/fruecker/emailer',
    keywords='email',
    install_requires=[
          'smtplib',
          'email'
      ],

)