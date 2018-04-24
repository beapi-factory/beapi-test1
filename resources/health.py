# Flask imports
from flask import g
from flask.ext import restful
from flask.ext.restful import marshal

# Flaskit imports
from flaskit import app
from flaskit.utils import ErrorNotFound
from flaskit.resource import MetaResource, init_api, generate_swagger_from_schema

# Python imports
import sys
import copy
import json



#=========================
# health swagger fields 
#=========================
@generate_swagger_from_schema(schemaRef="HealthGet", schemaPath="definitions/response/properties/results/items", type="Response")
class HealthGetResponseResultsFields:
    pass

@generate_swagger_from_schema(schemaRef="HealthGet", schemaPath="definitions/response/properties/_metadata", type="Response")
class HealthGetResponseMetadataFields:
    pass

@generate_swagger_from_schema(schemaRef="HealthGet", schemaPath="definitions/response", type="Response")
class HealthGetResponseFields:
    pass


##################################################################################################
# Health resource
##################################################################################################
class Health(MetaResource):
    """Manage health
    """
    @init_api("HealthGet")
    def get(self):
        """Health check

        Run health check

        TITLE:Sample
        <pre>
        CURL:"/_health"
        </pre>
        """

        self.initializeAPI()

        response = {
            "results": {
                "items": []
            },
            "_metadata": {}
        }

        # health check
        code = 200
        response["_metadata"]["status"] = 0

        return(response, code)
