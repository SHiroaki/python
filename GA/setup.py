from distutils.core import setup, Extension

module1 = Extension('cbinarymethods',
                    sources = ['cbinary.c'])

setup (name = 'cbinarymethods',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
