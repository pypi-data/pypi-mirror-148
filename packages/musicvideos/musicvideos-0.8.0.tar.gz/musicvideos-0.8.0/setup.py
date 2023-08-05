from setuptools import setup, find_packages

VERSION = '0.8.0'
DESCRIPTION = 'Old slowedvideos now musicvideos, Various scripts from justcow.'

# Setting up
setup(
    name="musicvideos",
    version=VERSION,
    author="JustCow",
    author_email="<justcow@pm.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['moviepy', 'pydub', 'pedalboard', 'yt_dlp', 'pillow', 'soundfile', 'requests', 
                    'google-api-python-client', 'google-auth-oauthlib', 'google-auth-httplib2', 'oauth2client', 'shutil'],
    keywords=['python', 'video', 'audio'],
    include_package_data=True ,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ]
)