#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# @authors   Christoph Dinh <christoph.dinh@brain-link.de>
# @version   1.0
# @date      April, 2022
# @copyright Copyright (c) 2022, BRAIN-LINK UG and authors of ScanHub Tools. All rights reserved.
# @license   BSD 3-Clause License
# @brief     AcquisitionControl
# ---------------------------------------------------------------------------

#%%
import os

###################################################################################################
# AcquisitionControl class
###################################################################################################

class AcquisitionControl(object):
    """the AcquisitionControl object

    Attributes:
        _first_scan_number (int): the first scan number
        _last_scan_number (int): the last scan number
    """

    ###############################################################################################
    # Constructor
    ###############################################################################################
    def __init__(self):
        """Return a new AcquisitionControl object."""
        self._first_scan_number = 0
        self._last_scan_number = 0
        self._num_scans = 0
        self._num_scans_to_acquire = 0
        self._num_scans_acquired = 0
        self._num_scans_to_save = 0
        self._num_scans_saved = 0
        self._num_scans_to_process = 0
        self._num_scans_processed = 0
        self._num_scans_to_delete = 0
        self._num_scans_deleted = 0
        self._num_scans_to_abort = 0
        self._num_scans_aborted = 0
        self._num_scans_to_retrieve = 0
        self._num_scans_retrieved = 0
        self._num_scans_to_resume = 0
        self._num_scans_resumed = 0
        self._num_scans_to_pause = 0
        self._num_scans_paused = 0
        self._num_scans_to_resume_from_pause = 0
        self._num_scans_resumed_from_pause = 0
        self._num_scans_to_pause_from_resume = 0
        self._num_scans_paused_from_resume = 0
        self._num_scans_to_abort_from_pause = 0
        self._num_scans_aborted_from_pause = 0
        self._num_scans_to_abort_from_resume = 0
        self._num_scans_aborted_from_resume = 0
        self._num_scans_to_abort_from_abort = 0
        self._num_scans_aborted_from_abort = 0
        self._num_scans_to_abort_from_retrieve = 0
        self._num_scans_aborted_from_retrieve = 0
        self._num_scans_to_abort_from_resume_from_pause = 0