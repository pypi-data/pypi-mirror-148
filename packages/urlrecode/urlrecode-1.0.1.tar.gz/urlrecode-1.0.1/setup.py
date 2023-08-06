from distutils.core import setup
import os

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='urlrecode',
    version='1.0.1',
    url='https://github.com/MKaterbarg/urlrecode',
    license='MIT',
    author='Martijn Katerbarg',
    packages=['urlrecode',],
    author_email='martijnkaterbarg@gmail.com',
    description='Simple URLEncode and URLDecode which I needed for a couple of bash scripts.',
    entry_points={
        'console_scripts': [
            'urlrecode = urlrecode.main:main',
        ],
    },
)
