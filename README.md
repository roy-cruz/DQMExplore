# DQMExplore

This repository hosts `dqmexplore`, a Python package which provides tools that facilitate the exploration of CMS DQM data for shifters, shift leaders & experts. These tools enable the evaluation of runs at a per-lumisection level. It utilized the [DIALS API](https://github.com/cms-DQM/dials-py) to access monitoring element histograms, as well as the [OMS API](https://gitlab.cern.ch/cmsoms/oms-api-client) to obtain information regarding the data taking conditions and trigger rate.

## Setup

The tools offered in this repo are meant to be primarily used in [SWAN](https://swan.web.cern.ch/swan/), but this project includes a `pyproject.toml` and `requirements.txt` which defines all of the dependencies, so you can set things up in your preferred way. However, if you are going to use the OMS API, you will need to be working inside the lxplus. Using this API also requires authentication. Please visit the official [OMS API repo](https://gitlab.cern.ch/cmsoms/oms-api-client/-/tree/master) for more information on the available authentication methods.

To setup DQMExplore, firstly:
1. Navigate to SWAN and click the "Download Project from git" button in the top right.
2. Insert the link to this repository, namely `https://github.com/CMSTrackerDPG/DQMExplore.git`, and click "Download". SWAN will automatically create a new project with all of the files from this repository.
3. Launch the notebook you wish to use. Template notebooks are found in the `DQMExplore/notebooks` directory. SWAN should already have all the depedencies you need except for the `omsapi` & `dqmplore` . Assuming you are in the `notebooks` subdirectory, to install them, simply run the following in your notebook.
    ```
    !pip3 install omsapi
    !pip3 install .. --no-dependencies
    ```
    If you are setting your virtual environment, assuming you are located in the project's root directory, you can install all the required libraries by running the following inside your environment.
    ```bash
    pip3 install poetry 
    poetry install -E oms -E nb
    ```

### Importing `cmsdials`

To import `cmsdials`, run the following in your notebook

```python
import cmsdials
from cmsdials.auth.client import AuthClient
from cmsdials.auth.bearer import Credentials
from cmsdials import Dials
from cmsdials.filters import LumisectionHistogram1DFilters, LumisectionHistogram2DFilters

auth = AuthClient()
token = auth.device_auth_flow()
creds = Credentials.from_authclient_token(token)

creds = Credentials.from_creds_file()
dials = Dials(creds)
```

Click on the link it provides and log in using your CERN account. Once you do that, come back to your notebook. For more information, please visit the [DIALS API repository](https://github.com/cms-DQM/dials-py).

### Instructions for obtaining OMS API Credentials

If you wish to use token authentication for OMS API, you can follow the following steps to obtain the credentials. More information can be found in the [OMS API repository](https://gitlab.cern.ch/cmsoms/oms-api-client/-/tree/master).

1. Navigate to to [this link]('https://application-portal.web.cern.ch/') and click "Add an Application".
2. Fill in the Application Identifier information. Generate it using a format such as `<yourusername>-oms-api` and include your name. The rest of the details are not necessary at this step. Proceed to SSO Registration.
3. Keep the protocol for authentication as OpenID Connect (OIDC). Generate a Redirect URI (e.g. `https://<yourusername>-oms-api.cern.ch`) and a Base URL (e.g. `https://<yourusername>-oms-dev.cern.ch`). Select the option: "My application will need to get tokens using its own client ID and secret".
Note: It is not necessary for these URLs to exist.
4. You should see your "CLIENT ID" and "CLIENT SECRET". Save them as these are the credentials you need. However, they can't be used until permission is granted.
5. Send an email to cmsoms-developers@cern.ch or cmsoms-operations@cern.ch to get the approval. Once it's granted, the OMS API credentials may be utilized.
