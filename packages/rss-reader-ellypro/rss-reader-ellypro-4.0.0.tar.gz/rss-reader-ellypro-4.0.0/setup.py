from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name='rss-reader-ellypro',
    version='4.0.0',
    author='Elyorbek Hamroyev',
    author_email='pro100elly@gmail.com',
    license='MIT',
    description='This cmd tool is intended to read rss-feed from realpython.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/EllyPro',
    py_modules=['helpers'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['rss_reader=rss_parser.rss_parser:main']
    }
)
