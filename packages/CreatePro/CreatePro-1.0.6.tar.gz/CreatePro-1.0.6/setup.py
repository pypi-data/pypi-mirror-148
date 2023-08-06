from setuptools import setup, find_packages


setup(
    name='CreatePro',
    version='1.0.6',
    author='CleverCreator',
    author_email='clevercreator@icloud.com',
    packages=find_packages(),
    zip_safe=True,
    platforms=['Linux', 'MacOS'],
    install_requires=[''],
    python_requires='>=3.9',
    description='A build tool',
    long_description='Seeing https://github.com/CleverCreater/BuildTools',
    license='MIT',
    url='https://github.com/CleverCreater/BuildTools',
    classifiers=[],
    scripts=['./entry.py']
)
            