# rpc_reader

[![PyPI version](https://img.shields.io/pypi/v/rpc-viewer.svg)](https://pypi.org/project/rpc-reader/)
[![Build Status](https://gitlab.com/t8237/rpc_viewer/badges/master/pipeline.svg)](https://gitlab.com/t8237/rpc_viewer/-/commits/master)
[![codecov](https://gitlab.com/t8237/rpc_viewer/badges/master/coverage.svg)](https://gitlab.com/t8237/rpc_viewer/-/commits/master)

A RPC III file is a data file conforming to the RPC III file specification developed by MTS corporation. This utility may be used to plot RPC data. 

This reader does not have the capacity to read all variants specified in the [documentation](https://corp.mts.com/cs/groups/public/documents/library/mts_007569.pdf) provided by MTS.

## Installation
This program can be installed from PyPi or from Gitlab.com
```bash
# From PyPi
python -m pip install rpc-viewer  

# From gitlab.com
python -m pip install git+https://gitlab.com/t8237/rpc_viewer.git
```


## Usage
### Python module

```python
import pathlib
from rpc_viewer.rpc_viewer import ViewRPC

# Set path to file
rpc_file_path = pathlib.Path('rpc_file_path.prc')

# Instantiate reader object
prc_object = ViewRPC(rpc_file_path)

# Import data, example to plot channel 0
prc_object.plot_channel(0)

# Print channel headers
prc_object.print_channel_header_data()
```

# Version history
## 0.1
 - Initial version

# Contribution and bug reports
Please use this issue tracker in the on gitlab.com for issues and enhancements!
[rpc-reader issues](https://gitlab.com/t8237/rpc_viewer/-/issues)  

## Contributors
Lukas Stockmann  
Niklas Melin
