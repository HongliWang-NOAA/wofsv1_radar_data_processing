import setuptools

from numpy.distutils.core import setup, Extension

#from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

#lib = Extension(name='wofs.post.cape', sources=['wofs/post/mod_rip_cape.pyf', 'wofs/post/mod_rip_cape.f'])

setup(
    name='wofs_radar', 
    #ext_modules = [lib],
    version="1.0",
    description='Warn-on-Forecast radar pre-processing',
    #long_description_content_type='text/markdown',  
    url='https://github.com/WarnOnForecast/wofs-obs-radar', 
    author='NOAA National Severe Storms Laboratory', 
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Scientists',
        'Programming Language :: Python :: 3'
    ],
    packages=['wofs_radar', 'wofs_radar.refl', 'wofs_radar.utils', 'wofs_radar.vr' ],  # Required
    #python_requires='>=3.5, <4',
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_dir={'wofs_radar': 'wofs_radar'},
    package_data={'': ['utils/*.so', '*.so']},
    # project_urls={  # Optional
    #     'Bug Reports': 'https://github.com/WarnOnForecast/wofs-obs-radar/issues',
    #     'Source': 'https://github.com/WarnOnForecast/wofs-obs-radar',
    # },
)