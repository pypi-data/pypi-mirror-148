import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nbabattle',
    version='0.0.6',
    license='MIT',
    description='A lightweight python library to generate two nba team battle image.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['nbabattle'],
    author='victor yang',
    author_email='victor.yang@hellosanta.com.tw',
    url='https://github.com/cobenash/nba-battle-picture-generator',
    project_urls = {
        "Bug Tracker": "https://github.com/cobenash/nba-battle-picture-generator/issues"
    },
    install_requires=['colorthief', 'Pillow'],
    keywords=["pypi", "nbabattle", "nba_battle"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={'': ['teams/*.png']},
)
