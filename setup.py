from distutils.core import setup
import re

name = "webtail"
verstrline = open(name, "rt").read()
versionre = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(versionre, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (name,))

setup(
    name=name,
    version=verstr,
    description='Tail your filesystem from the web.',
    long_description='Tail your filesystem from the web.',
    author='Olle Lundberg',
    author_email='geek@nerd.sh',
    license='MIT License',
    url='https://bitbucket.org/olle/webtail',
    scripts=[name],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: System :: Logging'
    ]
)
