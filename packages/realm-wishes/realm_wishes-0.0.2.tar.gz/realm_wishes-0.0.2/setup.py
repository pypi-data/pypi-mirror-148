from setuptools                         import setup, find_packages


setup(
    name='realm_wishes',
    version='0.0.2',
    license='MIT',
    author='Billy Katalayi',
    author_email='billysbn7@gmail.com',
    packages=find_packages('src'),
    package_dir={'' : 'src'},
    url='https://github.com/Billykat7/wishes',
    keywords='employees birthday, anniversary automated wishes',
    install_requires=[
        'celery',
        'redis',
        'requests',
        'SQLAlchemy'
    ],
)
