from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
        name="pyfping",
        version="1.0.1",
        description="fping-like python application",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/junka/pyfping",
        project_urls={
            "Bug Tracker": "https://github.com/junka/pyfping/issues",
        },
        author="junka",
        author_email="wan.junjie@foxmail.com",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: BSD License",
        ],
        packages=["pyfping"],
        package_dir={'pyfping':'src/pyfping'},
        entry_points={
            'console_scripts':[
                'pyfping=pyfping.ping:main',
            ]
        },
        python_requires=">=3.5",
)