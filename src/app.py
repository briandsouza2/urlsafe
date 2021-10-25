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
url_array = [line.strip() for line in open('teststrings.txt')]
url_set = set(url_array)

@app.route("/urlinfo/1/<hostname_and_port>/<original_path_and_query_string>")
def array_lookup(hostname_and_port, original_path_and_query_string):
    # Naive: use a for loop to determine if the URL is safe
    #for url in url_array:
    #    if url == original_path_and_query_string:
    #        return f"True"

    if original_path_and_query_string in url_array:
        return f"True"
    return f"False"

@app.route("/urlinfo/2/<hostname_and_port>/<original_path_and_query_string>")
def set_lookup(hostname_and_port, original_path_and_query_string):
    # Use a set to determine if the URL is safe    
    if original_path_and_query_string in url_set:
        return "True"
    return f"False"