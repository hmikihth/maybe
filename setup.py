import os
import glob
from distutils.command.build import build
from distutils.command.install_data import install_data
from setuptools import setup
import subprocess

PO_DIR = "po"
MO_DIR = "share/locale"
BASH_COMP_DIR = "/etc/bash_completion.d"

datafiles = []
datafiles.append((BASH_COMP_DIR, ["maybe_bc"]))

for po in glob.glob (os.path.join (PO_DIR, '*.po')):
    lang = os.path.basename(po[:-3])
    mo = os.path.join('build', MO_DIR, lang, 'LC_MESSAGES', 'maybe.mo')
    datafiles.append((MO_DIR, [mo]))
    directory = os.path.dirname(mo)
    if not os.path.exists(directory):
        print('creating %s' % directory)
        os.makedirs(directory)

    print('compiling %s -> %s' % (po, mo))
    try:
        rc = subprocess.call(['msgfmt', '-o', mo, po])
        if rc != 0:
            raise "Warning, msgfmt returned %d" % rc
    except:
            print ("Building gettext files failed.")
            print ("%s: %s" % (type(e), e))
            sys.exit(1)
                    
setup(
    name="maybe",

    version="0.4.0",

    description="See what a program does before deciding whether you really want it to happen.",
    long_description="For a detailed description, see https://github.com/p-e-w/maybe.",

    url="https://github.com/p-e-w/maybe",

    author="Philipp Emanuel Weidmann",
    author_email="pew@worldwidemann.com",

    license="GPLv3",

    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",

        "Topic :: Utilities",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: POSIX :: Linux",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="sandbox files access",

    packages=["maybe", "maybe.filters"],

    install_requires=[
        "six==1.10.0",
        "blessings==1.6",
        "python-ptrace==0.9.1",
    ],

    setup_requires=[
        "pytest-runner>=2.7",
    ],
    tests_require=[
        "pytest>=2.9.1",
    ],

    entry_points={
        "console_scripts": [
            "maybe = maybe.maybe:main",
        ],
    },

    data_files=datafiles,
)
