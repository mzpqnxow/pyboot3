## pyboot3

Use for developing and deploying Python3 projects on systems without relying on any OS packages or any other files in your local "profile". Completely repeatable and also contains **fully up to date** virtualenv, setuptools, pip which allows you to use new features of each. In some cases this is very important, e.g. support for pep517/518 and support for other types of "advanced" syntax in `requirements.txt`

### Using

Use `make python3`. There is no longer support for `python2`

### First Time Using

If this is your first time using pyboot, see the section "I Am New" at the end of this document

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

### I Am New

If you've never used pyboot3 before, there are some basic steps you should know. First, make sure you have `git` and `rsync` installed

```
$ sudo apt-get install git rsync
```

You *probably* already have them installed.. so you can just check using `which git` / `which rsync` before trying to install packages

#### Cloning pyboot3

Pyboot3 is not a `pip` installable package. It is a a metapackage meant for building `pip` installable packages. It's also suitable for using for deployments. To use it, you first must clone it. and enter the directory

```
$ git clone https://github.com/mzpqnxow/pyboot3 && cd pyboot3
```

At this point, you will want to "install" pyboot3 into your repository. It is best to do this with a fresh (empty) repository, since pyboot3 places some files in the root of the project. However, any files that are overwritten will be automatically backed up for you. To install into your repository, make sure that your `PATH` is set so that `which python3` returns the version of Python3 you want to use, in case you have multiple versions of Python3 on your system. Use the following command to kick the process off:

```
$ make new REPO=https://github.com/you/yournewproject
```

This command will clone *your* repository and then install the necessary files from pyboot3 into it using `rsync`. At some point, it will open your text editor and give you an opportunity to modify the `.git/config` file of your new repository. This is not necessary for 99% of cases and is really only intended for those who need to explicitly specify a `[user]` section, in case their `git` config name and/or email is not set correctly or at all. You can just quit the editor and let the process continue. You don't need to save the file, you can simply quit using your editor's quit command

At the end of this process, it will inform you where your checked out repository is. You'll want to make sure that it's not in a subdirectory of pyboot3 at that point since git will become confused. If necessary, move it to a fresh location. You can rename the directory of your project if you like.

You can now change directory into your project. When you list the directory, you will essentially see the same file structure that pyboot3 has. If you performed the `make new` operation on a repo that already contained files, make sure they are still present. You should now use:

```
$ git add .
```

This will add all of the newly added files to your local project. At this point, you can actually commit and push changes to your repository

$ git commit -m "Installing pyboot environment"
$ git push || echo "WARN: Not pushing changes"
$ git tag 0.0.1  # Recommended starting tag if you plan to use versioneer: 0.0.1
$ git push --tags
```

At this point, everything should be checked in and pushed to your central repository

**NOTE**: You should take a look at the `pyboot.backup.*` directory using `find pyboot.backup.*` to look for any files that may have been overwritten during the installation of pyboot3. Because pyboot3 uses specific filenames, there is a chance of a collision if you had files in your project with the same name. *This is why it is recommended to use `make new` on a fresh/new repository*

#### Preparing your project to be packaged

If you have any applications/scripts as a part of your project and you want them to be installed when your project is installed via `pip`, you should do the following:

```
$ mkdir bin/
$ cp your scripts bin/
$ git add -f bin
$ git commit bin -m 'adding scripts'
$ git push
```

In nearly all cases, you will have one or more package directories in your project. Packages are directories that contain an `__init__.py` file. You should copy your package directories into the root of the repository:

```
$ cp -r ~/code/mypackage mypackage
$ git add mypackage
$ git commit mypackage -m 'adding package'
```

For the rest of this guide, we will use `mypackage` as an example name for configuring `setuptools` (`setup.py` and `setup.cfg`) so that your project can be installed via `pip`

The next step to preparing your project for packaging is to edit both the `setup.py` and `setup.cfg` files. These are already filled out with boilerplate values. Most changes should be pretty obvious, such as the 

##### Filling in setup.py

You will need to change some boilerplate values in `setup.py` to fit your project. Again, we are assuming your package is called `mypackage`. Change the variables inside `setup.py` so that it looks more like this at the top:

```
PACKAGE = 'mypackage'
# Optionaly, you do not have to add "py" to the front of your package for the project name
# The project name can be anything you want and will be what pip uses to install it
# I prefer to add "py" to the beginning, but it's a matter of personal preference
PROJECT_NAME = 'py{}'.format(PACKAGE)

# Another optional setting
# I prefer to "namespace" packages, so that project squatting is not an issue and also to avoid
# colliding with an already existing project name. If you work for a company, you can use the
# ORG.OU.package project naming convention, e.g. exxon.engineering.mypackage
# Or, you can remove ORG, OU and NAMESPACE and set the following:
# NAME = PROJECT
#
# Ultimately, the NAME value is what pip will use to install your project
# If you left things like the example, you would install your project using:
# $ pip install company.group.mypackage
#
ORG = 'company'
OU = 'group'
NAMESPACE = [ORG, OU]
NAME = '.'.join(NAMESPACE + [PROJECT_NAME])

# Self-explanatory
AUTHOR = 'John Q. Doe'
EMAIL = 'jqdoe@company.com'
# Don't change this unless you know what you're doing
EXCLUDE_FILES = (
    '.keep',
    'constraints.txt',
    'interactive',
    'pip.ini',
    'pip.ini.socks')
LICENSE = 'Proprietary'
#
# If you would like to include data files, such as configuration files or other
# static content, you can specify the directories where those files reside
#
# In the example, you can either change the PACKAGE_DATA_DIRS to an empty list
# or specify the paths you've created with data in them. Remember you will need
# to mkdir these directories, place files in them, and add them to your repository
#
PACKAGE_DATA_DIRS = ['etc/mypackage']
PYTHON_REQUIRES = '>=3'

# Keep this in sync with venv/requirements-project.txt for a nice development experience
# If your package has dependencies, add them here, e.g.:
REQUIRED = ['pandas', 'psycopg2', 'sqlalchemy']
# If you have scripts, specify a list of them here. You can take a shortcut here and use
# Python's glob module, you can specify a list of paths manually, or you can set an empty
# list if you don't have any scripts that you want to be installed with your project
SCRIPTS = glob('bin/*')
```

The next thing you may need to change is the call to `setuptools.setup()` which does all of the work. If you don't intend to use `versioneer`, you should set the `version` argument to a version string, like `'0.0.1'`. If you are going to use versioneer, you will keep this as is. The rest you can leave the same without causing any issues. If you want the E-Mail and Author information in `setup.cfg` to be used, you can remove the `author` and `author_email` variables. If you are not going to use versioneer, you will also need to remove the `cmdclass` variable from the call to `setup()`


```
setup(
    author=AUTHOR,
    author_email=EMAIL,
    cmdclass=versioneer.get_cmdclass(),
    data_files=DATA_FILE_LIST,
    include_package_data=True,
    install_requires=REQUIRED,
    license=LICENSE,
    name=NAME,
    packages=find_packages(),
    python_requires=PYTHON_REQUIRES,
    scripts=SCRIPTS,
    version=versioneer.get_version())
```

At this point, you can move on to editing `setup.cfg`, which is used by many tools, including `setuptools`

##### Filling in setup.cfg

You should change the obvious things here, like the metadata bout your project name and description, author, e-mail, etc. The only other thing you will want to change is the `[versioneer]` section. If you do not plan to use `versioneer`, you can simply leave it as it is. If you *do* intend to use `versioneer`, I suggest changing the example `[versioneer]` section as follows:

```
[versioneer]
#---------------------------------------------------------------
# Change this next bit, I suggest you namespace your packages to
# avoid name collisions for private and public repositories
#----------------------------------------------------------------
# parentdir_prefix = company.org.
versionfile_source = mypackage/_version.py
versionfile_build = mypackage/_version.py
VCS = git
style = pep440
tag_prefix = 
```

Take note of the `parentdir_prefix` variable. You should set this to a value if you used namespacing in `setup.py. For example, if you set your namespace to be `exxon.engineering` then you will want to change the entry above to:

```
parentdir_prefix = exxon.engineering.
```

Note the trailing `.` which is important. If you are using versioneer but do not want to namespace your project, you can simply set it as:

```
parentdir_prefix = ''
```

#### Conclusion

That's pretty much everything. The last thing for you to do is run `versioneer install`, which will take the steps necessary to install `versioneer` based on the configuration you provided in `setup.cfg`. Once you have finished that, add the files `versioneer` created to your repository, commit them and push them

Once more .. if using versioneer, you can see if you did it correctly by using the `make release` command. The `release` target is provided by the pyboot3 `Makefile` and will automatically bump the minor version of your current `git tag` and then push it to git. This allows you to later install a specific version directly from GitHub using `pip` using the following:

```
$ pip install git+https://https://github.com/yourname/yourreponame@<tag/version or branch>#egg=<package>
```

Examples if you did not use namespacing:

```
git+https://https://github.com/yourname/yourreponame@master#egg=pymypackage
git+https://https://github.com/yourname/yourreponame@0.0.1#egg=pymypackage
```

If you *did* use namespacing, your examples will look like this:

```
git+https://https://github.com/yourname/yourreponame@master#egg=exxon.engineering.pymypackage
git+https://https://github.com/yourname/yourreponame@0.0.1#egg=exxon.engineering.pymypackage
```


### Tested Platforms

Tested on Linux x86_64, Linux ppc64le and MacOS. MacOS may require small changes in the `Makefile` for the lack of `realpath` on the OS

### Credits

Adam Greene <copyright@mzpqnxow.com>
David Marker

### License

(C) 2018 BSD 3-Clause
