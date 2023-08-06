import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "jsii-publish-test",
    "version": "0.13.1965",
    "description": "A dummy construct, used for automated testing of jsii-publish",
    "license": "MIT",
    "url": "https://github.com/udondan/jsii-publish",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Schroeder",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/udondan/jsii-publish.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "jsii_publish_test",
        "jsii_publish_test._jsii"
    ],
    "package_data": {
        "jsii_publish_test._jsii": [
            "jsii-publish-test@0.13.1965.jsii.tgz"
        ],
        "jsii_publish_test": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.21.1, <3.0.0",
        "jsii>=1.57.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
