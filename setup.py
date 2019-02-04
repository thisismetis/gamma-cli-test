from setuptools import setup, find_packages

setup(
    name='gamma',
    version='0.1.26',
    url='https://github.com/thisismetis/gamma-cli',
    author='soph',
    author_email='s@soph.info',
    packages=find_packages(),
    install_requires=[
        'Click',
        'Pandas',
        'path.py',
        'python-frontmatter',
        'beautifulsoup4',
        'jinja2',
        'xlsxwriter',
        'colorama',
        'tabulate',
        'gitpython',
    ],
    entry_points='''
        [console_scripts]
        gamma=gamma.main:gamma
    ''',
    include_package_data=True,
)
