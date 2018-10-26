from setuptools import setup

setup(
    name='MyProxy-Pool',
    version='2.0.0',
    description='High performance proxy pool',
    long_description='A proxy pool project modified from WiseDoge/ProxyPool',
    author=['Germey', 'WiseDoge', 'Xupeng'],
    author_email='1181714380@qq.com',
    url='https://github.com/Germey/ProxyPool',
    packages=[
        'proxy-pool'
    ],
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'requests',
        'flask',
        'redis',
        'pyquery'
    ],
    entry_points={
        'console_scripts': ['proxy_pool_run=run:cli']
    },
    license='apache 2.0',
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
