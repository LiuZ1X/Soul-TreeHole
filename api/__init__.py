#!/usr/bin/env python
# encoding: utf-8

import logging

from api import settings
from api.db.init_data import init_web_data
from api.utils import show_configs
from api.utils.log_utils import initRootLogger
from api.utils import file_utils

initRootLogger("resonant-soul")

logging.info(r"""
 ____              _   _____                _   _       _      
/ ___|  ___  _   _| | |_   _| __ ___  ___  | | | | ___ | | ___
\___ \ / _ \| | | | |   | || '__/ _ \/ _ \ | |_| |/ _ \| |/ _ \
 ___) | (_) | |_| | |   | || | |  __/  __/ |  _  | (_) | |  __/
|____/ \___/ \__,_|_|   |_||_|  \___|\___| |_| |_|\___/|_|\___|                                                                  
""")

logging.info(
    f'project base: {file_utils.get_project_base_directory()}'
)

show_configs()
settings.init_settings()
init_web_data()
