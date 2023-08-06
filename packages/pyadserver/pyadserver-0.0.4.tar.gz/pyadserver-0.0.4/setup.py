import setuptools


with open('README', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
        name='pyadserver',
        version='0.0.4',
        author_email='sga@kitech.re',
        description='Python package for Adserver team in KITECH',
        long_description_content_type='text/markdown',
        url='https://github.com/sga2022/',
        packages=setuptools.find_packages(),
        classifieres=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            ],
        python_requires='>=3.6',
        install_requires=[
            'numpy>=1.22.3',
            'scipy>=1.8.0',
            'matplotlib>=3.5',
            ],
        author='Seongbin Ga',
        )

