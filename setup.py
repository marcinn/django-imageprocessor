from setuptools import setup, find_packages

setup(name='netwizard-imageprocess',
        version='1.0',
        description='High-level layer for image processing using PIL',
        author='Marcin Nowak',
        author_email='marcin.j.nowak@gmail.com',
        packages=find_packages('src'),
        namespace_packages=['netwizard'],
        package_dir = {
            'netwizard': 'src/netwizard',
            }

        )

