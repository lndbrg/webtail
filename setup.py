from distutils.core import setup
import re
name="webtail"
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
    scripts=[name]
)
