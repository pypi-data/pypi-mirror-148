from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='botCreate',
    packages=find_packages(),
    version='1.0.0a',
    description='Create discord bots in python in only 10 seconds.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Artic#3065',
    license='MIT',
    url='https://github.com/ArticOff/botCreate',
    install_requires=['discord==1.7.3'],
    setup_requires=['pytest-runner'], 
    tests_require=['pytest'], 
    test_suite='tests',
    author_email="artic.admisoffi@gmail.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English'
    ]
)