# Semblance

> Personal Python project with the aim to learn more about OpenCV and Computer Vision to support my current**[Self-Driving Car Engineer ND](https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013)** in the School of **Autonomous Systems** studies. Code is based on [examples](https://github.com/PacktPublishing/Learning-OpenCV-4-Computer-Vision-with-Python-Third-Edition) accompanying this [book](https://www.packtpub.com/product/learning-opencv-4-computer-vision-with-python-3-third-edition/9781789531619).

## Getting Started

This project is made with

```bash
$ python --version
Python 3.8.5
```

and

```bash
$ pip --version
pip 20.2.3 from /Users/joustava/.asdf/installs/python/3.8.5/lib/python3.8/site-packages/pip (python 3.8)
```

and dependencies are manged with [pipenv](https://pipenv.pypa.io/en/latest/)

```bash
$ pip install --user pipenv
```

I use [fish](https://fishshell.com/) as my default shell and had to edit my PATH env to make it work, like

```bash
$ set -U fish_user_paths ~/.local/bin $fish_user_paths
$ pipenv --version
pipenv, version 2020.8.13
```

When all the above has been done succesfully the project dependencies need to be installed

```bash
$ pipenv
```

Then before starting to hack away, run the tests to see if everything works as expected.

```bash
make test
```

Run it with

```bash
make run
```

## Details

The project layout is based on chapter [Structuring Your Project](https://docs.python-guide.org/writing/structure/) of the book [The Hitchhiker’s Guide to Python!](https://docs.python-guide.org/).

On my developing environments I use either [docker](https://www.docker.com/) or [asdf](https://github.com/asdf-vm/asdf) (with the required plugins) to be able to run several versions of each language I work with.

Dependency management is done with [pipenv](https://pipenv.pypa.io/en/latest/), packages can be added and removed by running e.g `$ pipenv (un)install (--dev) requests`.

Documentation is generated with [sphinx](https://www.sphinx-doc.org/), on a mac you can install it by running
`brew install sphinx-do` (assuming you have homebrew installed).

Testing is awesome, checkout [Testing Your Code](https://docs.python-guide.org/writing/tests/) for basics.