# Unofficial CareHome.co.uk Python API client

Unofficial CareHome.co.uk API Client for Python.


## Installation

```
pip install carehomecouk
```


## Requirements

- Python 3.7+


# Usage

```Python

import datetime

from autumna.client import APIClient
from autumna.constants import Category
from autumna.resources.enquiry import Enquiry

api_client = APIClient('MY_API_KEY')

enquiries = Enquiry.many(
    api_client,
    date_time_from=datetime.datetime(2022, 4, 15),
    category_id=Category.CARE_ENQUIRY
)

for enquiry in enquiries:
    print(enquiry)

