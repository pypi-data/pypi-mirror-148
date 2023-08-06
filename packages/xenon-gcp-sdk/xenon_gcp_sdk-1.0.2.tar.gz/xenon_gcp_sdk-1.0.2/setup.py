from setuptools import setup, find_packages

setup(
    name='xenon_gcp_sdk',
    version='1.0.2',
    license='MIT',
    author="support",
    author_email='support@xenon.work',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/xenon-work/xenon',
    keywords='xenon cloud platform sdk',
    install_requires=[
        'google-cloud-secret-manager',
    ],

)
