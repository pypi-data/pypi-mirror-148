from setuptools import setup

setup(
    name='ppackexample',
    version='0.0.1',    
    description='A example Python package',
    url='https://github.com/shuds13/ppackexample',
    author='Bin Yang',
    author_email='bin.yang@polymtl.ca',
    license='BSD 2-clause',
    packages=['ppackexample'],
    install_requires=['numpy>=0.5',
                      'scipy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
