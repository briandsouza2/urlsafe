from flask import Flask
# from markupsafe import escape

app = Flask(__name__)

# Assumptions:
# The complete list of URLs can be loaded into memory
#
# The user will have no way to modify the URL list (it's immutable for now).
#
# Hostname and port will not be analyzed:
#   i.e. if <hostname>:<port-1>/<uri> is blocked it is NOT the case <hostname>:<port-2>/<uri> 
#   will be blocked (the only thing different between the URLs is port) 
# 
# Original_path and query_string will not be analyzed:
#   i.e. The following examples are assumed to be different:
#        download_file?param1=1&param2=2 
#        download_file?param2=2&param1=1 (parameters passed in different order)
#        download_file?param1=1&param2=2&pawned=3 (extra parameters passed in)
#   even though they will likely be poiting to the same resource
#  

global url_set
app.logger.debug('Initializes set')
url_set = set(line.strip() for line in open('/tmp/teststrings.txt'))

@app.route("/urlinfo/1/<hostname_and_port>/<original_path_and_query_string>")
def hello_world(hostname_and_port, original_path_and_query_string):
    # look up the URL
    if original_path_and_query_string in url_set:
        return "True"
    return f"False"
