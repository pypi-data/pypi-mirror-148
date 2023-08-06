from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='urlrecode',
    version='0.0.6',
    packages=[''],
    url='https://github.com/MKaterbarg/urlrecode',
    license='MIT',
    author='Martijn Katerbarg',
    author_email='martijnkaterbarg@gmail.com',
    description='Simple URLEncode and URLDecode which I needed for a couple of bash scripts',
    entry_points={
        'console_scripts': [
            'urlrecode = urlrecode:main',
        ],
    },
)
