#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

# Copyright (C) 2022 Wojtek Kosior <koszko@koszko.org>
#
# Available under the terms of Creative Commons Zero v1.0 Universal.

import setuptools

from setuptools.command.build_py import build_py

class CustomBuildCommand(build_py):
    '''
    The build command but runs babel before build.
    '''
    def run(self, *args, **kwargs):
        self.run_command('compile_catalog')
        super().run(*args, **kwargs)

setuptools.setup(cmdclass={'build_py': CustomBuildCommand})
