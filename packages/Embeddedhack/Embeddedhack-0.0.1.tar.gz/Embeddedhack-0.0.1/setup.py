from setuptools import setup
filepath="./README.md"

setup(name='Embeddedhack',
      version='0.0.1',
      description='This tool is used for backdoor and shellcode generation for various architecture devices',
      url='https://github.com/doudoudedi/hackEmbedded',
      author='doudoudedi',
      author_email='doudoudedi233@gmail.com',
      license='MIT',
      py_modules=['Embeddedhack.generate_arm','Embeddedhack.generate_mips',"Embeddedhack.generate_aarch64","Embeddedhack.extract_shellcode"],
      data_files=[filepath]
)

