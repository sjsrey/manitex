from setuptools import setup, find_packages


setup(
    name="manitex",
    version="0.2",
    packages=find_packages(),
    entry_points={'console_scripts': [
            'manitex = manitex.manitex:main',
        ]
    }
)
