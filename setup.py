from setuptools import setup, find_packages

setup(
    name='petit_ts',
    version='0.1.2',
    description='Convert your python types to typescript',
    packages=['petit_ts'],
    url='https://github.com/Plawn/petit_ts',
    license='apache-2.0',
    author='Plawn',
    author_email='plawn.yay@gmail.com',
    long_description="Look at the github",
    python_requires='>=3.8',
    install_requires=['executing'],
)
