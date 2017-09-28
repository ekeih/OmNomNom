from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as f:
        requirements_file = f.readlines()
    return [r.strip() for r in requirements_file]


setup(
    name='omnbot',
    version='2017.3',
    description='OmNomNom - A simple Telegram bot to get canteen information',
    long_description=readme(),
    url='https://omnbot.io',
    author='Max Rosin',
    author_email='omnbot@hackrid.de',
    license='AGPL',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3',
    install_requires=requirements(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'omnbot-worker=backend.backend:worker',
            'omnbot-housekeeping=backend.backend:housekeeping',
            'omnbot-beat=backend.backend:beat',
            'omnbot-frontend=frontend.frontend:main'
        ]
    }
)
