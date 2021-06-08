#!/bin/bash
python setup.py sdist build
file_name=`ls -lt ./dist | grep unicase-cli | head -n 1 | awk '{print $9}'`
echo dist/${file_name}
twine upload dist/${file_name}