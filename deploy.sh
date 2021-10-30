#!/bin/bash

# My effort at a custom-deployment script, that takes care of bumping versions
# where appropriate, making new commits into appropriate branches and creation
# of Git tags for each new release.

function error() {
    MESSAGE=$1
    echo -en "\n\033[31;1m${MESSAGE}\033[0m\n"
}

function success() {
    MESSAGE=$1
    echo -en "\n\033[32;1m${MESSAGE}\033[0m\n"
}

function info() {
    MESSAGE=$1
    echo -en "\n\033[34;1m${MESSAGE}\033[0m\n"
}


if [ -z $1 ]; then
    echo "A version number must be provided!"
    exit 1
fi

VERSION=$1

info "Making VERSION substitutions..."
sed -e "s/__VERSION_STR__/$VERSION/g" setup.py.in > setup.py


info "Calling build..."
python3 -m build

if [ $? -ne 0 ]; then
    error "There was a failure building the package!!!"
    exit 1
fi

success "Version $VERSION was built successfully."

# Deployment. Use 'twine', but call pip install --upgrade to ensure that we
# have, or can install, the latest Twine install.
info "Moving to PyPi deployment stage..."
info "Ensuring that twine is installed..."

python3 -m pip install --upgrade twine

if [ $? -ne 0 ]; then
    error "There was an issue when ensuring that the Twine Python package was present! Aborting."
    exit 1
fi

info "Uploading new release files to PyPy..."
info "Target files:"
ls -1 dist/texttab-0.5.5*.{whl,tar.gz}

python3 -m twine upload dist/texttab-0.5.5*.{whl,tar.gz}

if [ $? -ne 0 ]; then
    error "Upload to PyPi appears to have failed!!"
    exit 1
fi

success "Upload complete! Enjoy the newest version around."