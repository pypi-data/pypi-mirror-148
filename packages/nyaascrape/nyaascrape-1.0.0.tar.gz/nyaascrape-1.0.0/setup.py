from setuptools import setup

setup(
    name='nyaascrape',
    version='1.0.0',    
    description='Uses search terms to find data related to torrents and has a cli to download highest seeded torrent',
    url='https://github.com/cpiccirilli1/nyaascrape',
    author='Chelsea Piccirilli',
    author_email='piccirilli115@gmail.com',
    license='BSD 2-clause',
    packages=['nyaascrape'],
    install_requires=['requests', 'beautifulsoup4', 'random', 'pprint', 'webbrowser'                     
                      ],
    download_url="https://github.com/cpiccirilli1/nyaascrape/archive/refs/tags/v1.0.1.tar.gz",
    keywords = ['scrape', 'nyaa.si', 'nyaa', 'cli', 'torrent', 'anime'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    ],
)
