from setuptools import setup, find_packages

setup(
    name='gamma',
    version='0.1.6',
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
    package_data={"templates": ["*"]},
)
