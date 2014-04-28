"""Fabric configuration file."""

from fabric.api import local

SETTINGS = {
    'TEST_PACKAGES': ','.join([
        'lib',
    ]),
}


def clean():
    """Clean local directory from produced files."""
    local('find . -name "*.pyc" -delete')
    local("rm -rf cover/")
    local("rm -f .coverage")
    local("rm -f tags")


#------------------------------------------------------------------------------
# testing

def coverage():
    """Run coverage report."""
    local((
        "nosetests "
        " --with-coverage"
        " --cover-html"
        " --cover-branches"
        " --cover-inclusive"
        " --cover-package=%(TEST_PACKAGES)s"
        " --nocapture" % SETTINGS))


def test():
    """Run tests."""
    local((
        "nosetests "
        " --nocapture"))
