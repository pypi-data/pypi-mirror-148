from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.5'
DESCRIPTION = 'A simple Unicode based text crypter'

long_description = '''
# JUC
JUC is a simple Unicode based text crypter

[GitHub page](https://github.com/JProgrammer-it/JUC)


note: *You can find all the examples in the folder `examples`*


# Installation
For now this project is not on [pypi](https://pypi.org) ( pip ), so you have to install it manually by downloading the repo


# Preview
> ### Original and decrypted file differences
> ![Differences](https://github.com/JProgrammer-it/JUC/raw/main/assets/fileSize.PNG)
> The quality of the original file and the decrypted file is equal :)
> 
> ### Text Crypter
> ![TextCrypter](https://github.com/JProgrammer-it/JUC/raw/main/assets/TextCrypter.png)

# Examples

> ### Encrypting a text
> ```py
> from JUC import *
> worker = Juc('YourSecretKey')
> print(worker.crypt(b'ehy, hello there'))
> ```
> ### Decrypting a text
> ```py
> from JUC import *
> worker = Juc('YourSecretKey')
> print(worker.decrypt(text).decode())
> ```


> ### Encrypting a file
> ```py
> from JUC import *
> 
> worker = Juc('YourSecretKey')
> 
> filePath = 'image.png'
> 
> with open(f'result.png', 'wb') as f:
>     with open(filePath, 'rb') as file:
>         content = file.read()
>         crypted = worker.crypt(content)
>         f.write(crypted.encode())
> ```
> ### Decrypting a file
> ```py
> from JUC import *
> 
> worker = Juc('YourSecretKey')
> 
> filePath = 'result.png'
> fileType = filePath.split('.')[-1]
> 
> with open(filePath, 'r') as file:
>     content = file.read()
>     with open(f'result-decrypted.{fileType}', 'wb') as f:
>         decrypted = worker.decrypt(content, False)
>         f.write(decrypted)
> ```
'''

# Setting up
setup(
    name="JUC",
    version=VERSION,
    author="JProgrammer-it",
    author_email="<jprogrammer.mail@pm.me>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cryptography', 'encryption', 'decryption', 'text', 'file', 'unicode', 'python3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)