from setuptools import setup, find_packages

setup(
    name='gamma',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'Pandas', 'path.py', 'python-frontmatter', 'beautifulsoup4',
        'jinja2', 'xlsxwriter', "colorama"
    ],
    entry_points='''
        [console_scripts]
        gamma=gamma.main:gamma
    ''',
)
