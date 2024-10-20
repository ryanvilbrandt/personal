# Py2Exe version 6.3 setup file for wxPython GUI programs.
# Creates a single exe file.
# It's easiest to add this wxPython2Exe.py file into the same
# folder with the source file and an optional iconfile like "icon.ico"
# (if you add your own icon file, remove the comment in front of icon_resources).
# Simply change the filename to whatever you called your source file.
# Optionally edit the version info and add the name of your icon file.
# Now run wxPython2Exe.py ...
# Two subfolders will be created called build and dist.
# The dist folder contains your .exe file, MSVCR71.dll and w9xpopen.exe
# Your .exe file contains your code, all neded modules and the Python interpreter.
# The MSVCR71.dll can be distributed, but is often already in the system32 folder.

from distutils.core import setup
import py2exe
import sys


# enter the filename of your wxPython code file to compile ...
filename = "VampHelper.py"

# ... this creates the filename of your .exe file in the dist folder
##if filename.endswith(".py"):
##    distribution = filename[:-3]
##elif filename.endswith(".pyw"):
##    distribution = filename[:-4]

distribution = "VampHelper"


# if run without args, build executables in quiet mode
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources, edit to your needs
        self.version = "0.9.2.4"
        self.author = "Ryan Vilbrandt"
        self.copyright = "(c) 2011, Ryan Vilbrandt\nVampire: the Masqurade (c) White Wolf Studios"
        self.name = "Vampire Social Event Helper"

################################################################
# The manifest will be inserted as resource into your .exe.  This
# gives the controls the Windows XP appearance (if run on XP ;-)
#
# Another option would be to store it in a file named
# test_wx.exe.manifest, and copy it with the data_files option into
# the dist-dir.
#
##manifest_template = '''
##<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
##<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
##<assemblyIdentity
##    version="5.0.0.0"
##    processorArchitecture="x86"
##    name="%(prog)s"
##    type="win32"
##/>
##<description>%(prog)s Program</description>
##<dependency>
##    <dependentAssembly>
##        <assemblyIdentity
##            type="win32"
##            name="Microsoft.Windows.Common-Controls"
##            version="6.0.0.0"
##            processorArchitecture="X86"
##            publicKeyToken="6595b64144ccf1df"
##            language="*"
##        />
##    </dependentAssembly>
##</dependency>
##</assembly>
##'''
##
##RT_MANIFEST = 24

# description is the versioninfo resource
# script is the wxPython code file
# manifest_template is the above XML code
# distribution will be the exe filename
# icon_resource is optional, remove any comment and give it an iconfile you have
#   otherwise a default icon is used
# dest_base will be the exe filename
test_wx = Target(
    description = "Helps organize social events, blood bonds, boons, etc. for Vampire: the Masquerade",
    script = filename,
##    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=distribution))],
    dest_base = distribution)

################################################################

setup(
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 1}},
    zipfile = None,
    windows = [test_wx],
    )
