from setuptools import setup, find_packages

setup(
    name='xenon_gcp_sdk',
    version='1.0.5',
    license='MIT',
    author="support",
    author_email='support@xenon.work',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/xenon-work/xenon',
    keywords='xenon cloud platform sdk',
    install_requires=[
        'google-cloud-secret-manager',
        'firebase-admin==5.2.0',
        'google-cloud-firestore==2.3.4',
        'google-api-python-client==2.36.0',
    ],

)
