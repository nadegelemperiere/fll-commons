# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite for path following testing
# -------------------------------------------------------
# Nadège LEMPERIERE, @02 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check path classes functions
Library         ../keywords/data.py
Library         ../keywords/filter.py
Library         OperatingSystem

*** Variables ***
${EXCEL_DATA_FILE}                ${data}/sensors-data.xlsx

*** Test Cases ***

2.1 Ensure path is correctly followed when using perfect data north oriented
    [Tags]      Path
    ${data}     Load Data       ${EXCEL_DATA_FILE}    nn0rs    0    50
    ${result}   Apply Filter    ${data}

2.2 Ensure path is correctly followed when using perfect data north east oriented data
    [Tags]      Path
    ${data}     Load Data       ${EXCEL_DATA_FILE}    nn45rs    45    50
    ${result}   Apply Filter    ${data}

2.3 Ensure path is correctly followed when using noisy data north oriented
    [Tags]      Path
    ${data}     Load Data       ${EXCEL_DATA_FILE}    n0rs    0    50
    ${result}   Apply Filter    ${data}

2.4 Ensure path is correctly estimated when following a sinusoid
    [Tags]      Path
    ${data}     Load Data       ${EXCEL_DATA_FILE}    sinus    0    20
    ${result}   Apply Filter    ${data}
