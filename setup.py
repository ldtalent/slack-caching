import os
from setuptools import setup, find_packages
import shutil
import sys 
version = __import__('slack_cache').get_version()

def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
        return f.read()

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('slack_cache.egg-info')
    sys.exit()




setup(
    name = 'slack_cache',

    version = __import__('slack_cache').get_version(),
   
    url = 'https://github.com/AHmed Khatab/slack_cache',

    author = 'AHmed Khatab',
    author_email = 'b-b@dr.com',
    description = "ldr project to cache slack messages to work with.",
    long_description = get_long_description(),
    keywords = 'slack caching',
    tests_require = ['nose'],
    install_requires = [],
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
    ],

    # entry_points = {
    #     'console_scripts': [
    #         'slack_cache = slack_cache.main:main',
    #     ]
    # }
)
