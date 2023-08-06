import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "halloumi-cloudwatch-dashboard",
    "version": "1.1.0",
    "description": "halloumi-cloudwatch-dashboard",
    "license": "Apache-2.0",
    "url": "https://github.com/sentiampc/halloumi-cloudwatch-dashboard.git",
    "long_description_content_type": "text/markdown",
    "author": "Sentia MPC<support.mpc@sentia.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/sentiampc/halloumi-cloudwatch-dashboard.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "halloumi_cloudwatch_dashboard",
        "halloumi_cloudwatch_dashboard._jsii"
    ],
    "package_data": {
        "halloumi_cloudwatch_dashboard._jsii": [
            "halloumi-cloudwatch-dashboard@1.1.0.jsii.tgz"
        ],
        "halloumi_cloudwatch_dashboard": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-autoscaling>=1.110.0, <2.0.0",
        "aws-cdk.aws-cloudwatch>=1.110.0, <2.0.0",
        "aws-cdk.aws-elasticache>=1.110.0, <2.0.0",
        "aws-cdk.aws-elasticloadbalancingv2>=1.110.0, <2.0.0",
        "aws-cdk.aws-rds>=1.110.0, <2.0.0",
        "aws-cdk.core>=1.110.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.46.0, <2.0.0",
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
