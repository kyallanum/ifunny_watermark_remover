import setuptools
from ifunny_watermark_remover._version import __description__, __tool_name__, __version__

name = __tool_name__

setuptools.setup(
    name=name,
    entry_points={
        'console_scripts': [
            f'{name}={name}.__main__:main'
        ]
    },
    version=__version__,
    author="Kyal Lanum",
    author_email="kyallanum@gmail.com",
    description=__description__,
    url=f"https://github.com/kyallanum/{name}",
    license="LICENSE.txt",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    include_package_data=True,
    package_data={
        '': ['ifunny_watermark_remover/resources/watermark.jpg']
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)