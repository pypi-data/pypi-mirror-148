#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: set ts=4
#
# Copyright 2021-present Linaro Limited
#
# SPDX-License-Identifier: MIT

from tuxbake.models import OEBuild
from tuxmake.runtime import Terminated
import signal


def build(**kwargs):
    old_sigterm = signal.signal(signal.SIGTERM, Terminated.handle_signal)
    oebuild = OEBuild(**kwargs)
    # oebuild.validate()
    oebuild.prepare()
    oebuild.do_build()
    oebuild.do_cleanup()
    signal.signal(signal.SIGTERM, old_sigterm)
    return oebuild
