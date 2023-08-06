from setuptools import setup,find_packages


setup(
    name='devcloudcli',
    version='0.21',
    description='A CLI wrapper for Intel DevCloud Bench',    
    license='Proprietary - Intel',
    author="karthik kumaar",
    author_email='karthikx.kumaar@intel.com',
    #packages=['dc_cli','scripts'],
    packages=find_packages('dc_cli'),
    package_dir={'': 'dc_cli'},
    keywords='dc project',
    install_requires=[
          'cmd2',
          'pexpect',
      ],
    entry_points={"console_scripts":["dc_cli = src.dc_cli:main"]},
    python_requires=">=3.6",
)
