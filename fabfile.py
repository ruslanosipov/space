from fabric.api import local

settings = {
    'TEST_PACKAGES': ','.join([
        'lib',
    ]),
}


def clean():
    local('find . -name "*.pyc" -delete')
    local("rm -rf cover/")
    local("rm -f .coverage")


#------------------------------------------------------------------------------
# testing

def coverage():
    local((
        "nosetests "
        " --with-coverage"
        " --cover-html"
        " --cover-branches"
        " --cover-inclusive"
        " --cover-package=%(TEST_PACKAGES)s"
        " --nocapture" % settings))


def test():
    local((
        "nosetests "
        " --nocapture"))
