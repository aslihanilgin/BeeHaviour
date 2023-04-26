from distutils.core import setup
setup(
  name = 'analysing-bee-behaviour',
  packages = ['analysing-bee-behaviour'],
  version = '1.0',
  description = 'Analysing bumblee behaviour from videos',
  author = 'Aslihan Ilgin Okan',
  author_email = 'aslihanilgin@outlook.com',
  url = 'https://github.com/aslihanilgin/analysing-bee-behaviour.git',
  download_url = 'https://github.com/aslihanilgin/analysing-bee-behaviour.git',
  keywords = ['computer vision','ML','object detection','sample'],
  classifiers = [],
  install_requires=['roboflow','numpy', 'cv2', 'pandas'],
)