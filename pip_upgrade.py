import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    print dist
    call("pip install --upgrade " + dist.project_name, shell=True)
