#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# @authors   Christoph Dinh <christoph.dinh@brain-link.de>
# @version   1.0
# @date      April, 2022
# @copyright Copyright (c) 2022, BRAIN-LINK UG and authors of ScanHub Tools. All rights reserved.
# @license   BSD 3-Clause License
# @brief     DataStream
# ---------------------------------------------------------------------------

#%%
import os

###################################################################################################
# DataStream class
###################################################################################################

class DataStream(object):
    """the DataStream object

    Attributes:
        _large_memory (bool): whether large memory configuration is choosen
    """
    
    _large_memory = True # If all epoch data fit into the Ram
    
    ###############################################################################################
    # Constructor
    ###############################################################################################
    def __init__(self):
        """Return a new DataStream object."""
        self._large_memory = True


###################################################################################################
# DataStreamError class
###################################################################################################

class DataStreamError(object):
    """the DataStreamError object

    Attributes:
    
    """
    
    ###############################################################################################
    # Constructor
    ###############################################################################################
    def __init__(self):
        """Return a new DataStreamError object."""


###################################################################################################
# DataStreamWarning class
###################################################################################################

class DataStreamWarning(object):
    """the DataStreamWarning object

    Attributes:
    
    """
    
    ###############################################################################################
    # Constructor
    ###############################################################################################
    def __init__(self):
        """Return a new DataStreamWarning object."""