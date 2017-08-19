# Let's get this party started!
import falcon
from postgres import pg as PGDB



print(PGDB)

PGDB().master()

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(PGDB):
    def on_get(self, req, resp):
        """Handles GET requests"""
        result = self.master().query("select * from tbl_test2;")
        print("after running query")
        # records = result.getAllRecords();
        print("after fetching records")
        # print(records)
        result = self.slave().query("select * from tbl_test2;")
        records = result.getAllRecords();
        print(records)

        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')
        print("at the end")

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
# things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', ThingsResource())

