#!/bin/bash
# -------------------------------------------------------
# Copyright (c) [2022] Nadege Lemperiere
# All rights reserved
# -------------------------------------------------------
# Scripts to analyze python code quality
# -------------------------------------------------------
# Nadège LEMPERIERE, @19 october 2022
# Latest revision: 19 october 2022
# -------------------------------------------------------

# Retrieve absolute path to this script
script=$(readlink -f $0)
scriptpath=`dirname $script`

docker run -v $scriptpath/..:/home/ technogix/terraform-python-awscli:v2.0.0 pylint --rcfile=/home/.pylintrc /home/commons