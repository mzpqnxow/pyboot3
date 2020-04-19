## pyboot3

Use for developing and deploying Python3 projects on systems without relying on any OS packages or any other files in your local "profile". Completely repeatable and fully up to date virtualenv, setuptools, pip

### Using

Use `make python3`. There is no longer support for `python2`

### Versioning / Developing / Publishing / Releasing

Set up versioneer using `versioneer install` and edit `setup.cfg` to get it correctly configured. Tag manually once with `git tag 0.0.1 && git push --tags`. From that point on, use `make release` for an auto-bump of the version and a push to your git repository using `versioneer`

#### Publishing via Twine

Twine is now the tool of choice to publish Python packages. The lines are currently commented out in the `release` / `publish` `Makefile` targets but can easily be re-enabled. You'll need a .pypirc file set up to publish. There is an example `.pypirc` file called `.pypirc.template` in the root of the repository. You can use `make pypirc` to automatically set it up for your user


### Deployments

Settings for your development and deployment dependencies are in `venv/`

* venv/constraints.txt (constraints file for forcing dependencies to use specific versions / forks / tags
* venv/requirements-base.txt (development assistance packages, e.g. pep8, isort, ipython.. disable for deploy)
* venv/requirements-project.txt (dependencies specific to your project)
* venv/requirements.txt (metafile, just includes the base and project requirements)

### Other Settings

* etc/pip.ini (standard pip configuration file, will be used for your virtual environment, add things like proxy settings, repositories, etc. here)

### TODO / NOTES

Random stuff

#### Notes From pip Documentation

Yeah, there's lots of useful and not as useful things you can do. Here are a few of those.

##### Bundling of Requirements for a Virtualenv Blob Requiring No Index

Pack it up:

```
$ tempdir=$(mktemp -d)
$ pip wheel -r venv/requirements.txt --wheel-dir=$tempdir
$ cwd=`pwd`
$ (cd "$tempdir"; tar -cjvf "$cwd/bundled.tar.bz2" *)
```

Unpack/install it:

```
$ tempdir=$(mktemp -d)
$ (cd $tempdir; tar -xvf /path/to/bundled.tar.bz2)
$ pip install --force-reinstall --ignore-installed --upgrade --no-index --no-deps $tempdir/*
```

Personally, I don't do this nor do I plan to


### Tested Platforms

Tested on Linux x86_64, Linux ppc64le and MacOS. MacOS may require small changes in the `Makefile` for the lack of `realpath` on the OS

### Credits

Adam Greene <copyright@mzpqnxow.com>
David Marker

### License

(C) 2018 BSD 3-Clause
