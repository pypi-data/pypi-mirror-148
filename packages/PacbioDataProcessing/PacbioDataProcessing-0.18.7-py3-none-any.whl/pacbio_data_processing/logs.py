#######################################################################
#
# Copyright (C) 2020, 2021 David Palao
#
# This file is part of PacBio data processing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################


import logging


DEFAULT_LOGGING_LEVEL = logging.INFO


def config_logging(verbosity):
    level = DEFAULT_LOGGING_LEVEL
    if verbosity:
        level = logging.DEBUG
    logging.basicConfig(
        level=level, format="[%(asctime)-15s][%(levelname)s] %(message)s")
    # logging to a file goes like:
    # fh = logging.FileHandler('spam.log')
    # fh.setLevel(logging.DEBUG)
    # logger = logging.getLogger()
    # logger.addHandler(fh)
