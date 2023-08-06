from setuptools import setup, find_packages

classifiers =[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name ='ExtractBlockchain',
    version="0.0.1",
    description="Extract data from any Blockchain using python",
    Long_discription =open('README.md').read()+'\n\n'+ open("CHANGELOG.txt").read(),
    url="",
    author ="Tushar Choudhary and Aakash deep",
    author_email="tusharchoudhary0003@gmail.com",
    License ="MIT",
    classifiers =classifiers,
    keywords ="Blockchain",
    packages=find_packages(),
    install_requires =[""]
)   