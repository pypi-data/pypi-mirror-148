from setuptools import setup, find_packages


setup(
    name='sdj_toolbox',
    version='0.3.0',
    license='MIT',
    author="Steve De Jongh",
    author_email='dejongh.st@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitea.irisib.be/sdejongh/sdj_toolbox.git',
    keywords='python toolbox helpers',
    install_requires=[
      ],

)
