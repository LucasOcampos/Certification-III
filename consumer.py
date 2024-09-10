import requests
from robocorp import workitems
from robocorp.tasks import task
from RPA.JSON import JSON
from RPA.Tables import Tables

json = JSON()
table = Tables()

TRAFFIC_JSON_FILE_PATH = "output/traffic.json"

# JSON data keys
COUNTRY_KEY = "SpatialDim"
YEAR_KEY = "TimeDim"
RATE_KEY = "NumericValue"
GENDER_KEY = "Dim1"

@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System robot.
    Consumes traffic data work items.
    """
    
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        if len(traffic_data["country"]) == 3:
            status, return_json = post_traffic_data_to_sales_system(traffic_data)
            if status == 200:
                item.done()
            else: 
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_FAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(
                exception_type="BUSINESS",
                code="INVALID_TRAFFIC_DATA",
                message=item.payload,
            )

def post_traffic_data_to_sales_system(traffic_data):
    url = "https://robocorp.com/inhuman-insurance-inc/sales-system-api"
    response = requests.post(url, json=traffic_data)
    return response.status_code, response.json()
