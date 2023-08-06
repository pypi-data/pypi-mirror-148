# Copyright (c) 2021, University of Washington
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the University of Washington nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF WASHINGTON AND CONTRIBUTORS
# “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF WASHINGTON OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from sliderule import icesat2
import logging

###############################################################################
# GLOBALS
###############################################################################

# create logger
logger = logging.getLogger(__name__)

###############################################################################
# APIs
###############################################################################

#
#  ICEPYX ATL06
#
def atl06p(ipx_region, parm, asset=icesat2.DEFAULT_ASSET):
    """
    create a sliderule atl06p query from an icepyx region
    """

    try:
        version = ipx_region.product_version
        resources = ipx_region.avail_granules(ids=True)[0]
    except:
        logger.critical("must supply an icepyx query as region")
        return icesat2.__emptyframe()
    # try to get the subsetting region
    if ipx_region.extent_type in ('bbox','polygon'):
        parm.update({'poly': to_region(ipx_region)})

    return icesat2.atl06p(parm, asset, version=version, resources=resources)

#
#  ICEPYX ATL03
#
def atl03sp(ipx_region, parm, asset=icesat2.DEFAULT_ASSET):
    """
    create a sliderule atl03sp query from an icepyx region
    """

    try:
        version = ipx_region.product_version
        resources = ipx_region.avail_granules(ids=True)[0]
    except:
        logger.critical("must supply an icepyx query as region")
        return icesat2.__emptyframe()
    # try to get the subsetting region
    if ipx_region.extent_type in ('bbox','polygon'):
        parm.update({'poly': to_region(ipx_region)})

    return icesat2.atl03sp(parm, asset, version=version, resources=resources)

def to_region(ipx_region):
    """
    extract subsetting extents from an icepyx region
    """
    if (ipx_region.extent_type == 'bbox'):
        bbox = ipx_region.spatial_extent[1]
        poly = [dict(lon=bbox[0], lat=bbox[1]),
                dict(lon=bbox[2], lat=bbox[1]),
                dict(lon=bbox[2], lat=bbox[3]),
                dict(lon=bbox[0], lat=bbox[3]),
                dict(lon=bbox[0], lat=bbox[1])]
    elif (ipx_region.extent_type == 'polygon'):
        poly = [dict(lon=ln,lat=lt) for ln,lt in zip(*ipx_region.spatial_extent[1])]
    return poly
