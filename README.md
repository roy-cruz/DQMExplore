# DQMExplore

This repository hosts `dqmexplore`, a Python software package that provides tools to facilitate the exploration of CMS DQM data for shifters, shift leaders, and experts. These tools enable the evaluation of runs at a per-lumisection level by allowing the user to plot 1D and 2D monitoring elements as well as trends in these using data obtained from the [DIALS Python API](https://github.com/cms-DQM/dials-py). In addition, it provides notebooks to facilitate the use data from sources such as OMS, Run Registry and CertHelper is a programatic way.

## Setup

The tools offered in this repo are meant to be primarily used in [SWAN](https://swan.web.cern.ch/swan/). The tools provided by `dqmexplore` can be used by either installing it as a Python package, for which a `pyproject.toml` and `requirements.txt` are included, or by adding `src/` to the system path and importing it.

### Accessing and Plotting Data with `dqmexplore` & `cmsdials`

In `src/utils/setupdials.py`, the small function `setup_dials_object_deviceauth()` ([original source](https://github.com/cms-DQM/dials-py/blob/develop/tests/integration/utils.py)) is included. This function will automate the setup of DIALS so you can start accesing ME data easily. Here is an example usage where we use it to access some PixelPhase1 1D monitoring elements for run 380238:

```python
import sys
sys.path.append("../src/")

# Setup DIALS
from utils.setupdials import setup_dials_object_deviceauth
dials = setup_dials_object_deviceauth()

# Query
runnb = 380238
me__regex =  "PixelPhase1/Tracks/PXBarrel/charge_PXLayer_." 

data1D = dials.h1d.list_all(
    LumisectionHistogram1DFilters(
        run_number = runnb,
        dataset__regex = "ZeroBias",
        me__regex = me__regex
    ),
    # max_pages=200
).to_pandas() # Returns a Dataframe
```

When run, this will prompt the user to follow a link which, when clicked will open a webpage which will prompt you to log in using your CERN account. One logged in, click "Yes" when it asks if you want to grant access privileges to cms-dials-prod-confidential-app. Once that is done, come back to your notebook. For more information, please visit the [DIALS Python API repository](https://github.com/cms-DQM/dials-py).

For examples on how to use the tools provided by `dqmexplore` to plot the data obtained from `cmsdials`, please refer to the notebooks found in `notebooks/`.