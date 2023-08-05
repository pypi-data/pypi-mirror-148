from distutils.core import setup
import setuptools
setup(name='DlxTestPack',  #打包后的包文件名
      version='1.2',
      description='UsedForSimcom AutoTest,Used environment python3.8.10', #说明
      author='hardfood',
      author_email='mdzzdyxc@163.com',
      url='https://www.cnblogs.com/hardfood',
      py_modules=['DlxTestPack.InI_DealV2','DlxTestPack.DlxTestClassV5',
                  'DlxTestPack.DlxEnhanced.CMW500','DlxTestPack.DlxEnhanced.P66391D',
                  'DlxTestPack.DlxEnhanced.SP9500','DlxTestPack.DlxEnhanced.UXM',
                  'DlxTestPack.DlxEnhanced.NB500Enhanced.NB',
                  'DlxTestPack.pack','DlxTestPack.TkPackByMe.guiFrame',
                  'DlxTestPack.TkPackByMe.fix','DlxTestPack.TkPackByMe.sqlite_api',
                  'DlxTestPack.TkPackByMe.time_test'],   #你要打包的文件
      install_requires=[
        'configobj','pyvisa','subprocess','pyserial'
    ],
)
#python setup.py build
#python setup.py sdist
#twine upload dist/*
