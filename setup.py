from distutils.core import setup

setup(
    name='specularity_removal',
    packages=['specularity_removal'],
    version='0.1.1',
    description='Implements specular removal in images captured from various view points',
    long_description=open('README.md').read(),
    author='Michael Jaison Gnanasekar, Shreyas Joshi',
    author_email='gmichaeljaison@gmail.com, shreyasvj25@gmail.com',
    url='https://github.com/gmichaeljaison/specularity-removal',
    download_url='https://github.com/gmichaeljaison/specularity-removal/tarball/0.1',
    keywords=['computer vision', 'image processing', 'specularity-removal',
              'highlights', 'homography'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
    requires=['numpy', 'cv2'],
    license='LICENSE'
)
