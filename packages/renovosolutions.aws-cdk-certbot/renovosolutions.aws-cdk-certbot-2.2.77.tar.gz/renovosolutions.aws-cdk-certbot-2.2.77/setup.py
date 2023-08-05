import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "renovosolutions.aws-cdk-certbot",
    "version": "2.2.77",
    "description": "AWS CDK Construct Library to manage Lets Encrypt certificate renewals with Certbot",
    "license": "Apache-2.0",
    "url": "https://github.com/RenovoSolutions/cdk-library-certbot.git",
    "long_description_content_type": "text/markdown",
    "author": "Renovo Solutions<webmaster+cdk@renovo1.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/RenovoSolutions/cdk-library-certbot.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "certbot",
        "certbot._jsii"
    ],
    "package_data": {
        "certbot._jsii": [
            "cdk-library-certbot@2.2.77.jsii.tgz"
        ],
        "certbot": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.21.1, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.57.0, <2.0.0",
        "publication>=0.0.3",
        "renovosolutions.aws-cdk-one-time-event>=2.0.48, <3.0.0"
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
