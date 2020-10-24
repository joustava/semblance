from setuptools import find_packages, setup

setup(
    name="semblance",
    description='OpenCV Learning',
    version='0.1',
    author='Joost Oostdijk',
    author_email='joustava@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src')
)
