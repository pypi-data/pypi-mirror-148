from setuptools import setup, find_packages

with open("README.md", "r") as fp:
    long_desc = fp.read()

setup(
    name="pcs-get",
    version="0.9.1",
    license='GPLv3+',
    author="zhoujianwei.garen",
    author_email="zhoujianwei.garen@bigo.com",
    description="the spider for pcs-protocol",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://git.sysop.bigo.sg/zhoujianwei.garen/pcs-get",
    packages=["pcsget"],
    keywords=["pcs", "bigo", "spider"],
    entry_points={
        'console_scripts': ['pcs-get=pcsget:execute']
    },
    classifiers=[
        'Environment :: Console',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Chinese (Simplified)",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7"
    ],
    install_requires=['requests~=2.25.1', 'lxml~=4.4.2'],
    python_requires='>=2.5',
)
