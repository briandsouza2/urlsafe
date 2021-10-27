from flask import Flask
from flask import request, jsonify
import os, fnmatch
import zipfile
from flask_cors import CORS
import logging
from flask import current_app, g
# from markupsafe import escape
from urllib.parse import urlparse, urlencode
from urllib.parse import parse_qs

app = Flask(__name__)
CORS(app)

global url_dict_set

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


def load_data_dict():
    app.logger.debug("Loading data")
    #import pdb; pdb.set_trace()
    url_dict_set = {}
    data_dir = './data'
    # go through the data folder and load all data
    for root, dirs, files in os.walk(data_dir):
        dirs.sort()
        for dirname in dirs:
            for _, _, files in os.walk(os.path.join(root, dirname)):
                files.sort()
                for name in files:
                    filename=os.path.join(root, dirname, name)
                    app.logger.debug("Dir name: %s, File name: %s", dirname, filename)
                    url_array = [line.strip() for line in open(filename)]
                    url_dict_set[dirname] = set(url_array)
    return url_dict_set

url_dict_set=load_data_dict()

@app.route("/urlinfo/1/<hostname_and_port>/<original_path_and_query_string>")
def set_lookup(hostname_and_port, original_path_and_query_string):
    # Use a set to determine if the URL is safe
    #app.logger.debug("dict: %s", url_dict_set)
    #app.logger.debug("query_string: %s", original_path_and_query_string)
    #import pdb; pdb.set_trace()
    if hostname_and_port in url_dict_set.keys():
        if original_path_and_query_string in url_dict_set[hostname_and_port]:
            return jsonify({'Blocked': True})
    return jsonify({'Blocked': False})

@app.route("/urlinfo/2/<hostname_and_port>/<original_path_and_query_string>")
def param_parse(hostname_and_port, original_path_and_query_string):
    # Use a set to determine if the URL is safe
    # normalize the original_path_and query
    parts=urlparse(original_path_and_query_string)
    query_params=parse_qs(parts.query)
    sorted_params = [f"{key}={query_params[key][0]}" for key in sorted(query_params)]
    query_params_sorted = "&".join(sorted_params)
    query_string = parts.path + "?" + query_params_sorted
    #param_names = list(query_params.keys())
    #param_names.sort()
    #query_params_sorted = ''
    #for param_name in param_names:
    #    query_params_sorted = query_params_sorted + param_name + '=' + query_params[param_name]
    #import pdb; pdb.set_trace()
    if hostname_and_port in url_dict_set.keys():
        if query_string in url_dict_set[hostname_and_port]:
            return jsonify({'Blocked': True, 'Match:': query_string})
    return jsonify({'Blocked': False})

# def main():
#     #load_data()
#     #app.run(threaded=False, processes=1)
#     app.logger.debug("In app::main")
#     app.run(host="0.0.0.0")

# if __name__=="__main__":
#     main()

#if __name__=="urlsafe.app":
#    app.logger.debug("In urlsafe.app")

#     #gunicorn_error_logger = logging.getLogger('gunicorn.error')
#     #app.logger.handlers.extend(gunicorn_error_logger.handlers)
#     app.logger.setLevel(logging.DEBUG)
#     load_data()

def create_app(test_config=None):

    if test_config:
        app.config.from_mapping(test_config)
    return app
    
def init_app():
    url_dict_set=load_data_dict()