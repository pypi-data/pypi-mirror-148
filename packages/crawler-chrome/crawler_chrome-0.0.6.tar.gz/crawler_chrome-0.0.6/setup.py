import os
from setuptools import setup

with open("./README.md", "rb") as fh:
    long_description = fh.read()

install_requires = []
if os.path.exists("./requirements.txt"):
    with open("./requirements.txt", "r") as fh:
        install_requires = fh.readlines()
        install_requires = [str(a).replace("\n", "") for a in install_requires]

setup(
    name='crawler_chrome',
    version='0.0.6',
    description='采集工具',
    author='hammer',
    author_email='liuzhuogood@foxmail.com',
    long_description=str(long_description, encoding='utf-8'),
    long_description_content_type="text/markdown",
    packages=['crawler_chrome'],
    package_data={'crawler_chrome': ['README.md', 'LICENSE', "requirements.txt", "add.js"]},
    install_requires=install_requires or []
)
