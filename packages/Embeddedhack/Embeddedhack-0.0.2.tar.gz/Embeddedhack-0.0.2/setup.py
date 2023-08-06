from setuptools import setup
filepath="./README.md"
readme_data=open("./README.md").read()


setup(name='Embeddedhack',
      version='0.0.2',
      description='This tool is used for backdoor and shellcode generation for various architecture devices',
      long_description=readme_data,
      long_description_content_type="text/markdown",
      url='https://github.com/doudoudedi/hackEmbedded',
      author='doudoudedi',
      author_email='doudoudedi233@gmail.com',
      license='MIT',
      py_modules=['Embeddedhack.generate_arm','Embeddedhack.generate_mips',"Embeddedhack.generate_aarch64","Embeddedhack.extract_shellcode"],
      data_files=[filepath]
)

