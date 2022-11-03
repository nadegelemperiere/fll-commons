""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Real time logger that can either print log as they
# are produced or store them in a file until the end of
# the program happens and they are reloaded and read.
# -------------------------------------------------------
# Each "print" call on spike takes roughly 50ms, due to
# the time required to connect from the hub to the laptop,
# send data, display...
# When dealing to real time processing (servomecanisms),
# the logging time may reduce significantly the
# computation frequency, which results in lack of
# precision and robustness.
# Storing the log in memory and print them after the real
# time processing is not possible either, due to the
# limited memory size of the hub.
# The best solution is to write them on file, and reread
# them at the end of the execution, line per line to
# avoid memory saturation, and print them when we have
# plenty of time
# -------------------------------------------------------
# Nadège LEMPERIERE, @02 november 2022
# Latest revision: 02 november 2022
# --------------------------------------------------- """

# System includes
from os import remove, listdir

class Logger :
    """ Real time logger  """

    m_shall_print_at_once   = True

    m_timer                 = None

    m_logs                  = None
    m_topics                = []

    m_filename              = ''

# pylint: disable=W0102, R1732
    def __init__(self, timer, shall_print_at_once = False, topics=[], filename='logs.txt') :
        """ Constructor
        ---
        timer (obj)                 : Timer for time measurement (matching spike timer interface)
        shall_print_at_once (bool)  : True if logs shall be printed as soon as they are issued
        topics (list)               : List of topics to be logged (if none, all will be logged)
        """

        self.m_shall_print_at_once      = shall_print_at_once
        self.m_timer                    = timer
        self.m_topics                   = topics
        self.m_filename                 = filename

        # Opening the file to store logs if they shall be stored rather than printed on the spot
        if not self.m_shall_print_at_once :
            self.m_logs = open(self.m_filename,'w', encoding='UTF-8')
            self.m_logs.write('######################## LOGS ##############################')

        self.m_timer.reset()

# pylint: enable=W0102, R1732

    def __del__(self) :
        """ Destructor
        ---
        """

        self.summarize()
        self.remove()

    def log(self, header, topic, message, shall_trace=True) :
        """ Log appending function
        ---
        header (str)        : Logging header
        topic(str)          : Topic to which the message belongs
        message(str)        : Message to write
        shall_trace(bool)   : True if message shall be logged, False otherwise
        """

        if shall_trace :
# pylint: disable=C0209
            seconds = str("{:.4f}".format(self.m_timer.now()))
# pylint: enable=C0209
            if topic in self.m_topics or len(self.m_topics) == 0 :
                full_message = header + ' [' + seconds + 's] - ' + topic + ' : ' + message
                if self.m_shall_print_at_once   : print(full_message)
                else                            : self.m_logs.write(full_message + '\n')

    def summarize(self) :
        """ Retained logs printing function"""

        if not self.m_shall_print_at_once :

            # Close the log file
            if self.m_logs is not None :
                self.m_logs.close()
                self.m_logs = None

            if self.m_filename in listdir() :
                # Open log file and print it line after line
                with open(self.m_filename,'r', encoding='UTF-8') as self.m_logs:
                    for line in self.m_logs :
                        print(line)
                self.m_logs.close()
                self.m_logs = None

    def remove(self) :
        """ Remove log file"""

        if not self.m_shall_print_at_once :

            if self.m_filename in listdir() and self.m_logs is None:
                remove(self.m_filename)

class ObjectWithLog :
    """ Object providing standardized log functions """

    m_name         = ''
    m_shall_trace  = False
    m_logger       = None
    m_trace_header = ''

    def __init__(self, name, logger, shall_trace = False, header='---') :
        """ Contruct generic object
        ---
        name (str)          : Name to use for object
        logger (obj)        : Logger to use for log collection
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        header (str)        : Trace header
        """

        self.m_shall_trace      = shall_trace
        self.m_trace_header     = header
        self.m_logger           = logger
        self.m_name             = name

    def log(self, message, header=''):
        """ Log message
        ---
        message (str)       : Message to log
        header (str)        : Additional header to use (optional)
        """
        self.m_logger.log(self.m_trace_header + header,self.m_name,message,self.m_shall_trace)
