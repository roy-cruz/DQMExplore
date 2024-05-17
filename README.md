# DQMExplore

This repository hosts tools that enable DQM shifters to evaluate runs at a per-lumisection level by utilizing the [DIALS API](https://github.com/cms-DQM/dials-py) access monitoring element histograms, as well as the OMS API, from which the shifter can get information regarding the data taking conditions, trigger rate, etc.

## Setup

The tools offered in this repo are meant to be primarily used in [SWAN](https://swan.web.cern.ch/swan/), but this project includes a `pyproject.toml` which defines all of the dependencies, so you can set things up in your preferred way (just keep in mind that it needs to be inside the lxplus). This setup also assumes that you already have OMS API credentials. If you do not have them, check the instructions below to see how you can do this.

To setup DQMExplore, firstly:
1. Navigate to SWAN and click the "Download Project from git" button in the top right.
2. Insert the link to this repository, namely `https://github.com/roy-cruz/DQMExplore.git`, and click "Download". SWAN will automatically create a new project with all of the files from this repository.
3. To the root directory of this project, add a json file for the OMS API credentials with the following contents
    ```json
    {
        "API_CLIENT_ID": "<your_client_id>",
        "API_CLIENT_SECRET": "<your_client_secret"
    }
    ```
4. Launch the notebook you wish to use. Template notebooks are found in the `DQMExplore/notebooks` directory. SWAN should already have all the depedencies you need except for the OMS API. To install it, simply run the following in your notebook.
    ```
    !pip3 install git+https://github.com/roy-cruz/OMSapi.git
    ```

### Importing `cmsdials` 

To import `cmsdials`, simply run the following in your notebook

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

### Importing `oms`

To import `oms` to be able to use the OMS API, run the following in your notebook.

```python
import json
import os

with open("../clientid.json", "r") as file:
    secrets = json.load(file)

os.environ["API_CLIENT_ID"] = secrets["API_CLIENT_ID"]
os.environ["API_CLIENT_SECRET"] = secrets["API_CLIENT_SECRET"]

import oms

oms_fetch = oms.oms_fetch()
```

Note that these commands assume you have the `clientid.json` file which contains your credentials one directory above the current working directory of the notebook. These commands will read the credentials, load them as environment variables, and when you `import oms`, the library will read the environment variables and allow you to access the OMS API.

### Instructions for obtaining OMS API Credentials

1. Navigate to 'https://application-portal.web.cern.ch/' and click "Add an Application".
2. Fill in the Application Identifier information. Generate it using a format such as "<yourusername>"-oms-api and include your name. The rest of the details are not necessary at this step. Proceed to SSO Registration.
3. Keep the protocol for authentication as OpenID Connect (OIDC). Generate a Redirect URI, for example, https://"<yourusername>"-oms-api.cern.ch and a Base URL, for example, https://"<yourusername>"-oms-dev.cern.ch. Select the option: "My application will need to get tokens using its own client ID and secret."ch. Last option to choose here :  My application will need to get tokens using its own client ID and secret and submit it.
Note: It is not necessary for these URLs to exist. 
4. You should see your "CLIENT ID" and "CLIENT SECRET". Save them as these are the credentials you need. However, you can't use them until you get permission.
5. Email to cmsoms-developers@cern.ch or cmsoms-operations@cern.ch. Afetr you get the approval, you can use your OMS API credentials. 
