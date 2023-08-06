# Avalara.SDK
API for evaluating transactions against direct-to-consumer Beverage Alcohol shipping regulations.

This API is currently in beta.


- Package version: 2.4.29

## Requirements.

Python >= 3.6

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import Avalara.SDK
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import Avalara.SDK
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

import time
import Avalara.SDK
from pprint import pprint
from Avalara.SDK.api import age_verification_api
from Avalara.SDK.model.age_verify_failure_code import AgeVerifyFailureCode
from Avalara.SDK.model.age_verify_request import AgeVerifyRequest
from Avalara.SDK.model.age_verify_result import AgeVerifyResult
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = Avalara.SDK.Configuration(
    username = 'YOUR USERNAME',
    password = 'YOUR PASSWORD',
    environment='sandbox'
)

# Enter a context with an instance of the API client
with Avalara.SDK.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = age_verification_api.AgeVerificationApi(api_client)
    age_verify_request = AgeVerifyRequest(
        first_name="first_name_example",
        last_name="last_name_example",
        address=AgeVerifyRequestAddress(
            line1="line1_example",
            city="city_example",
            region="region_example",
            country="US",
            postal_code="postal_code_example",
        ),
        dob="dob_example",
    ) # AgeVerifyRequest | Information about the individual whose age is being verified.
simulated_failure_code = AgeVerifyFailureCode("not_found") # AgeVerifyFailureCode | (Optional) The failure code included in the simulated response of the endpoint. Note that this endpoint is only available in Sandbox for testing purposes. (optional)

    try:
        # Determines whether an individual meets or exceeds the minimum legal drinking age.
        api_response = api_instance.verify_age(age_verify_request, simulated_failure_code=simulated_failure_code)
        pprint(api_response)
    except Avalara.SDK.ApiException as e:
        print("Exception when calling AgeVerificationApi->verify_age: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AgeVerificationApi* | [**verify_age**](docs/AgeVerificationApi.md#verify_age) | **POST** /api/v2/ageverification/verify | Determines whether an individual meets or exceeds the minimum legal drinking age.
*ShippingVerificationApi* | [**deregister_shipment**](docs/ShippingVerificationApi.md#deregister_shipment) | **DELETE** /api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registration | Removes the transaction from consideration when evaluating regulations that span multiple transactions.
*ShippingVerificationApi* | [**register_shipment**](docs/ShippingVerificationApi.md#register_shipment) | **PUT** /api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registration | Registers the transaction so that it may be included when evaluating regulations that span multiple transactions.
*ShippingVerificationApi* | [**register_shipment_if_compliant**](docs/ShippingVerificationApi.md#register_shipment_if_compliant) | **PUT** /api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/registerIfCompliant | Evaluates a transaction against a set of direct-to-consumer shipping regulations and, if compliant, registers the transaction so that it may be included when evaluating regulations that span multiple transactions.
*ShippingVerificationApi* | [**verify_shipment**](docs/ShippingVerificationApi.md#verify_shipment) | **GET** /api/v2/companies/{companyCode}/transactions/{transactionCode}/shipment/verify | Evaluates a transaction against a set of direct-to-consumer shipping regulations.


## Documentation For Models

 - [AgeVerifyFailureCode](docs/AgeVerifyFailureCode.md)
 - [AgeVerifyRequest](docs/AgeVerifyRequest.md)
 - [AgeVerifyRequestAddress](docs/AgeVerifyRequestAddress.md)
 - [AgeVerifyResult](docs/AgeVerifyResult.md)
 - [ErrorDetails](docs/ErrorDetails.md)
 - [ErrorDetailsError](docs/ErrorDetailsError.md)
 - [ErrorDetailsErrorDetails](docs/ErrorDetailsErrorDetails.md)
 - [ShippingVerifyResult](docs/ShippingVerifyResult.md)
 - [ShippingVerifyResultLines](docs/ShippingVerifyResultLines.md)


## Documentation For Authorization


## BasicAuth

- **Type**: HTTP basic authentication


## Bearer

- **Type**: API key
- **API key parameter name**: Authorization
- **Location**: HTTP header


## Author




## Notes for Large OpenAPI documents
If the OpenAPI document is large, imports in Avalara.SDK.apis and Avalara.SDK.models may fail with a
RecursionError indicating the maximum recursion limit has been exceeded. In that case, there are a couple of solutions:

Solution 1:
Use specific imports for apis and models like:
- `from Avalara.SDK.api.default_api import DefaultApi`
- `from Avalara.SDK.model.pet import Pet`

Solution 2:
Before importing the package, adjust the maximum recursion limit as shown below:
```
import sys
sys.setrecursionlimit(1500)
import Avalara.SDK
from Avalara.SDK.apis import *
from Avalara.SDK.models import *
```

