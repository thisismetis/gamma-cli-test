from setuptools import setup, find_packages
import gamma

setup(
    name='gamma',
    version=gamma.__version__,
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
    ],
    entry_points='''
        [console_scripts]
        gamma=gamma.main:gamma
    ''',
    include_package_data=True,
)
