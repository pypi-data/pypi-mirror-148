from setuptools import setup

setup(
    name='cameo_claw',
    version='1.2.4',
    description='Multiprocessing download, filter, streaming. ⚡️FAST⚡️ remove pandas',
    url='https://github.com/bohachu/cameo_claw',
    author='Bowen Chiu',
    author_email='bohachu@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_claw'],
    install_requires=[
        'requests==2.23.0',
        'polars==0.13.24',
        'tqdm==4.63.1',
        'fastapi==0.75.0',
        'uvicorn==0.17.6',
        # 'pandas==1.4.1',
        'filelock==3.6.0',
        'glob2==0.7',
        'Jinja2==2.10.1',
        'pyarrow==7.0.0',
        'httpx==0.22.0',
        # 'asyncio==3.4.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
