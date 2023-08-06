from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pyws2812',  # 包名
    version='0.1.2',  # 版本号
    description='A small example package',
    long_description=long_description,
    author='xf_zhan',
    author_email='zxf9972009@qq.com',
    url='https://github.com/phoenixsfly/pyWS2812',
    install_requires=['pyserial'],
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers', 'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)', 'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
