from setuptools import setup

with open('readme.md', 'r') as f :
    readme_content = f.read()

setup(
    name='petit_ts',
    version='0.2.2',
    description='Convert your python types to typescript',
    packages=['petit_ts'],
    url='https://github.com/Plawn/petit_ts',
    license='apache-2.0',
    author='Plawn',
    author_email='plawn.yay@gmail.com',
    long_description=readme_content,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    install_requires=['petit_type_system>=0.3.0'],
)
