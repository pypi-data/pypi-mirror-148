
from distutils.core import setup


# This call to setup() does all the work
setup(
    name="phpipam_pycli",
    packages=["phpipam_pycli"],
    version="0.0.2",
    description="Package to use phpipam api",
    author="Moosigno",
    author_email="moosigno.msg@protonmail.com",
    license="GNU",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=[],
)