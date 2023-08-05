from setuptools import setup

setup(
    name='cameo_claw',
    version='1.2.0',
    description='Multiprocessing download, filter, streaming. ⚡️FAST⚡️',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'requests',
        'polars',
        'tqdm',
        'fastapi',
        'uvicorn',
        'pandas',
        'filelock',
        'glob2',
        'jinja2',
        'pyarrow',
        'httpx',
        'asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
