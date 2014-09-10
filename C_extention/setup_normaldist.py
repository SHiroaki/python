from distutils.core import setup, Extension

module1 = Extension('_normaldist',
                    sources = ['normaldist_wrap.c', 'normaldist.c'])

setup (name = 'normaldist',
       version = '1.0',
       description = 'This is a normaldist package',
       ext_modules = [module1],
       py_modules = ["normaldist"],)
