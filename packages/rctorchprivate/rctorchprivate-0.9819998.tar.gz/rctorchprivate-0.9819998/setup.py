from distutils.core import setup
#from setuptools import setup, Extension

#read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

#this_file = Path(__file__).parent
#print(this_directory)
#long_description = this_file#.read_text()



setup(
  name = 'rctorchprivate',         # How you named your package folder (MyLib)
  packages = ['rctorchprivate'],   # Chose the same as "name"
  version = '0.9819998',      # Start with a small number and increase it with every change you make
  license='Harvard',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='A Python 3 toolset for creating and optimizing Echo State Networks. This library is an extension and expansion of the previous library written by Reinier Maat: https://github.com/1Reinier/Reservoir',# Give a short description about your library
  author = 'Hayden Joy',                   # Type in your name
  author_email = 'hnjoy@mac.com',      # Type in your E-Mail
  url = 'https://github.com/blindedjoy/RcTorch-private',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/blindedjoy/RcTorch/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Echo State Network', 'ESN', 'Reservoir Computing', 'Echo State Networks', 'Optimization', 'BoTorch', 'PyTorch', 'Bayesian'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
          'paramz',
          #'datetime',
          'pandas',
          'seaborn',
          'pathlib',
          'matplotlib',
          #'llvmlite',
          'torch',
          'torchvision',
          'torchaudio',
          'gpytorch',
          'botorch',
          #'ray' #[default]
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.6',
  ],
  long_description=long_description,
  long_description_content_type='text/markdown'

)

