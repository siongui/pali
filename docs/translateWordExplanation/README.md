# Development

<i>PALI_DIR</i> below means the directory where you git clone <em>pali</em> repository.

1. git clone the [pali](https://github.com/siongui/pali) repository and [data](https://github.com/siongui/data) repository (put in the same directory).
```bash
    # create a directory to contain both pali and data repository.
    $ mkdir dev
    $ cd dev
    # git clone repositories
    $ git clone https://github.com/siongui/pali.git
    $ git clone https://github.com/siongui/data.git
```

2. Create information of dictionaries.
```bash
    $ cd PALI_DIR/common/pytools/
    $ python setupdev.py
    $ python dic1parseBooks.py
```

3. Install [goslate](https://pypi.python.org/pypi/goslate)
```bash
    $ sudo pip install goslate
```

