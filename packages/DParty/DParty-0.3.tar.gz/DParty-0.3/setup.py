from setuptools import setup, find_packages

setup(name='DParty',
      version='0.3',
      descrption='Smart home SDK from DParty',
      author='lolisky',
      author_email='lorisky1214@gmail.com',
      requires=['mediapipe', 'cv2'],
      packages=find_packages(),
      license="apache 3.0")