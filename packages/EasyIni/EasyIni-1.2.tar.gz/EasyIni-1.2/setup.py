from distutils.core import setup,Extension
import setuptools


#https://stackoverflow.com/questions/57191483/include-a-dll-in-python-module-pypi
setup(name='EasyIni',  #打包后的包文件名
      version='1.2',
      description='UsedFor IniFile,Used environment python3.8.10', #说明
      author='hardfood',
      author_email='mdzzdyxc@163.com',
      url='https://www.cnblogs.com/hardfood',
      py_modules=['EasyIni.ini'],   #你要打包的文件
      # ext_modules=[

      #   Extension(name="tx",sources=['EasyIni/libs/inilib.dll'])#,libraries=[]
      # ],
      install_requires=[
        
    ],
)
#python setup.py build
#python setup.py sdist
#twine upload dist/*
