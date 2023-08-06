# Ceader

Tool for automatically adding a header to files in the form of a comment.\
Based on the file extensions, Ceader detects the programming language and selects the comment character accordingly.

Header sample, created by [this](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20) software:


```
                    _                _
   ___ ___ _ __ ___| |__  _ __ ___  (_) ___
  / __/ _ \ '__/ _ \ '_ \| '__/ _ \ | |/ _ \
 | (_|  __/ | |  __/ |_) | | |  __/_| | (_) |
  \___\___|_|  \___|_.__/|_|  \___(_)_|\___/

Proprietary software created by CEREBRE.
© CEREBRE, USA. All rights reserved.
Visit us at: https://www.cerebre.io
```



### Installation
From [PyPi](https://pypi.org/project/ceader/)
```
pip install ceader
```
### Exemplary cli usage
```
ceader --mode add_header --files-dir ${FILES_DIR} --header-path ${HEADER_PATH} --extensions ${EXTENSIONS} --debug --skip-hidden
```

### Pre-commit plugin
In order to use ceader in pre-commit add the following configuration to your .pre-commit-config.yaml:
```
repos:
    - repo: https://github.com/cerebre-io/ceader
        rev: 0.0.4
        hooks:
        - id: ceader
            args:[
                '--mode', ${MODE},
                '--files-dir', ${FILES_DIR},
                '--header-path', ${HEADER_PATH},
                '--extensions-list', ${EXTENSIONS},
                '--debug',
                '--skip-hidden',
                '--']
```
[pre-commit](https://pre-commit.com/) is a framework based on passing filenames to executables, but for now we need to turn it off, beacuse we are passing path to directory./
It is worth noting that pre-commit will change the headers of files that have been modified by us in the given commit, so if you want to change all files use CLI.

###### FILES_DIR
This is the path to the folder where the files need to be changed.\
In this folder, files will be searched recursively.

###### HEADER_PATH
Path to the file in .txt format with the header to be added.

###### EXTENSIONS
Files with these extensions will be searched for in the ${FILES_DIR}. \
The programming language will be recognized by this information and an appropriate comment will be added. For example:

TODO add a list of working extensions

###### DEBUG
An optional boolean value that allows checking the status of adding headers.

###### SKIP_HIDDEN
An optional boolean that allows you to ignore hidden files, even if they meet the extension condition.


###### MODE

There are two modes at the moment:\
    - ```add_header``` adds the indicated header to files, if header already exists in the file it does nothing.\
    - ```remove_header``` removes the indicated header to files, but only if header exists in the file.




### TODO

- pre-commit plugin
- user validation
- files backup
