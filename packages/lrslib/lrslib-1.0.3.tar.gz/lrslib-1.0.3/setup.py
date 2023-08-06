# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


setup(
    name="lrslib",
    version="1.0.3",
    description="这是lrslib",
    long_description="""
这是LRSLIB
里面有许多好用的功能
祝你好运~
//GitHub : github.com/lrsgzs/lrslib

Doc   文档
'tkin.Window':'对Tk()进行优化的适合中国人的一个类',
'tools.pront':'一个一个地打印文本',
'tools.show_image':'显示图片在pygame窗口中'
'by':'关于'
'func':'帮助'
""",
    include_package_data=True,
    author="Lrs",
    author_email="liurongshuo2022@outlook.com",
    url="https://github.com/lrsgzs/lrslib",
    packages=find_packages(),
    install_requires=['pygame','pillow'],
    extras_require={},
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    python_requires='>=3.7'
)
