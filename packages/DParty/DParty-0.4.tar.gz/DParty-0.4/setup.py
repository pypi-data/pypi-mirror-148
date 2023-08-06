from setuptools import setup, find_packages

setup(name='DParty',
      version='0.4',
      descrption='Smart home SDK from DParty',
      author='lolisky',
      author_email='lorisky1214@gmail.com',
      url="https://github.com/lorisky1214/DParty",
      requires=['mediapipe', 'cv2'],
      packages=find_packages(),
      license="apache 3.0")