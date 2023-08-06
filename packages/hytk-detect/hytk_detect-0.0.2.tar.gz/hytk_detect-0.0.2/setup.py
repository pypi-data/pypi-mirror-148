from setuptools import find_packages, setup


setup(
    name='hytk_detect',#需要打包的名字
    version='v0.0.2',#版本
    author='xuhua.ren',
    author_email='renxuhua1993@gmail.com',
    url='https://github.com/xuhuaren',
    packages=find_packages(),
    install_requires=[
     "numpy==1.19.4"
    ,"Pillow==8.0.0"
    ,"requests==2.25.1"
    ,"requests-oauthlib==1.3.0"
    ] ,
    include_package_data=True
)









