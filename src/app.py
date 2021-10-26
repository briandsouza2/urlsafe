from flask import Flask
from flask import request, jsonify
import os, fnmatch
import zipfile
# from markupsafe import escape

app = Flask(__name__)

# Assumptions:
# The complete list of URLs can be loaded into memory
#
# The user will have no way to modify the URL list (it's immutable for now).
#
# The input data is NOT case sensitive:
#   i.e. the following are the same:
#        download_file?param1=FILE1
#        download_file?param1=file1
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

global url_dict_array
global url_dict_set
app.logger.debug('Initializes set')
url_dict_set = {}
url_dict_array = {}

def load_data():
    # go through the data folder and load all data
    for root, dirs, files in os.walk('../data'):
        dirs.sort()
        for dirname in dirs:
            for _, _, files in os.walk(os.path.join(root, dirname)):
                files.sort()
                for name in files:
                    filename=os.path.join(root, dirname, name)
                    app.logger.debug("File name: %s", filename)
                    url_array = [line.strip() for line in open(filename)]
                    url_dict_array[dirname] = url_array
                    url_dict_set[dirname] = set(url_array)
                    

@app.route("/urlinfo/1/<hostname_and_port>/<original_path_and_query_string>")
def array_lookup(hostname_and_port, original_path_and_query_string):
    # Naive: use a for loop to determine if the URL is safe
    #for url in url_array:
    #    if url == original_path_and_query_string:
    #        return f"True"
    app.logger.debug('A value for debugging')
    if hostname_and_port in url_dict_array.keys():
        if original_path_and_query_string in url_dict_array[hostname_and_port]:        
            return jsonify({'Blocked': True})
    return jsonify({'Blocked': False})


@app.route("/urlinfo/2/<hostname_and_port>/<original_path_and_query_string>")
def set_lookup(hostname_and_port, original_path_and_query_string):
    # Use a set to determine if the URL is safe
    if hostname_and_port in url_dict_set.keys():
        if original_path_and_query_string in url_dict_set[hostname_and_port]:
            return jsonify({'Blocked': True})
    return jsonify({'Blocked': False})

def main():
    load_data()
    app.run(host="0.0.0.0")

if __name__=="__main__":
    main()