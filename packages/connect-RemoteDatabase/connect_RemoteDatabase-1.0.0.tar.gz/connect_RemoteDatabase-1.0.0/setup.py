# !/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(name='connect_RemoteDatabase',  # 包名
      version='1.0.0',  # 版本号
      description='连接一个远端的Mysql数据库',
      long_description='输入用户名，密码，要连接到数据库名称，将为你连接到一个远端数据库',
      # 包的介绍，因为这个里面的内容是显示在pypi包首页上
      author='curchy',
      author_email='',
      url='',
      license='',
      install_requires=['pymysql'],
      # 申明依赖包，安装包时pip会自动安装
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )

