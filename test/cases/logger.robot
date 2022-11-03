# -------------------------------------------------------
# TECHNOGIX
# -------------------------------------------------------
# Copyright (c) [2022] Technogix SARL
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite for iam compliance with the
# CIS Amazon Web Services Three Tier Benchmark v1.0.0
# -------------------------------------------------------
# Nadège LEMPERIERE, @27 october 2021
# Latest revision: 27 october 2021
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check real time logger efficiency
...             We compare writing the logs as they go, and keep them
...             in a file and print it at the end. On a standard computer
...             the second is slower than the first, which is not the
...             case on spike where writing a log require sending it to
...             the laptop and lasts 50 ms.
Library         ../keywords/logger.py

*** Variables ***

*** Test Cases ***

1.1 Ensure logs are processed quickly when written on the spot
    ${result}            Log And Print During 100 Iterations
    ${speed}             Compute Logging Speed    ${result}
    Should Be True       ${speed} > 1000

1.2 Ensure logs are processed quickly when kept until the end of the program
    ${result}            Log And Retain During 100 Iterations
    ${speed}             Compute Logging Speed    ${result}
    Should Be True       ${speed} > 1000

1.3 Ensure logger enable filter by topic
    @{topics} =          Create List    Whatever
    ${result}            Log Selected Topics During 100 Iterations    @{topics}
    Length Should Be     ${result}    61
    @{topics} =          Create List    test
    ${result}            Log Selected Topics During 100 Iterations    @{topics}
    Length Should Be     ${result}    9661
