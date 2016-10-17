from setuptools import setup

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Framework :: Twisted",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
]

if __name__ == "__main__":
    with open('README.md') as f:
        readme = f.read()

    setup(
        name="txsessionmgr",
        packages=['txsessionmgr',],
        version="1.0.0",
        install_requires=[
            "Twisted",
        ],
        author="Zenoss Solutions",
        author_email="solutions@zenoss.com",
        classifiers=classifiers,
        description="Manager for keeping track of single login sessions.",
        url="https://github.com/zenoss/txsessionmgr",
        long_description=readme
    )
