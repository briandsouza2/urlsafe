
 A simple service that can be queried to determine if a given URL is safe to allow access to.

 The query can be made using REST calls with the following format:

   /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}

It will return "True" if the given input results in a safe URL or false otherwise.