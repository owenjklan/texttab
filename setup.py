from distutils.core import setup
setup(
  name = 'texttab',         # How you named your package folder (MyLib)
  packages = ['texttab'],   # Chose the same as "name"
  version = '0.5.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Create ASCII tables that are flexible. Colours, various border styles and custom column formatters are some of the features.',   # Give a short description about your library
  author = 'Owen Klan',                   # Type in your name
  author_email = 'owen.j.klan@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/owenjklan/texttab',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/owenjklan/texttab/archive/refs/tags/v0.5.0.tar.gz',    # I explain this later on
  keywords = ['command-line', 'ascii', 'tables', 'formatters', 'extensible'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    # Because we heavily use f-strings, a python 3.6 feature
    'Programming Language :: Python :: 3.6',
  ],
)