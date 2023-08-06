from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Message Encryption & Decryption With Morse Code.'
LONG_DESCRIPTION = 'A package that allows you to encrypt and decrypt morse code.'

# Setting up
setup(
    name="whatmorse",
    version=VERSION,
    author="GodZilo (Ido Barel)",
    author_email="<vikbarel5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'morse', 'code',
              'encryption', 'crypto'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
