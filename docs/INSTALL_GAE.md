# Install Necessary Tools for Development

1. See this [Stack Overflow question](http://stackoverflow.com/questions/7214474/how-to-keep-up-with-the-latest-versions-of-nodejs-in-ubuntu-ppa-compiling) to install the latest version of [node.js](http://nodejs.org/).

2. See [Getting Started](http://gruntjs.com/getting-started) to install [Grunt](http://gruntjs.com/).

3. Install Linux tools on local machine.
```bash
    sudo apt-get install git-all
    sudo apt-get install gettext
```

4. (optional) Install [Open Chinese Convert](https://code.google.com/p/opencc/) and [pyOpenCC](https://pypi.python.org/pypi/pyopencc) to convert between Traditional Chinese and Simplified Chinese.
```bash
    # install pyopencc (on Ubuntu 13.04)
    sudo apt-get install libopencc-dev python-dev
    git clone https://github.com/cute/pyopencc.git
    cd pyopencc
    python setup.py build_ext -I /usr/include/opencc/
    sudo python setup.py install
```

   Usage Example:
```bash
    import pyopencc
    cc = pyopencc.OpenCC('zhs2zht.ini')
    Traditional_Chinese_string = cc.convert(Simplified_Chinese_string)
```

   Google Search keyword: "python traditional chinese to simplified chinese". Similar tools: [OpenCC-Python](https://bitbucket.org/victorlin/opencc_python), [python-jianfan](https://code.google.com/p/python-jianfan/).
