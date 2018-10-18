json_config - Simple configuration manager
==========================================

Intended to handle multiple configuration files (of the same name) in various locations


Usage
-----

Simple case

::

    from json_config import JsonConfig

    conf = JsonConfig.new_conf(logger=self.logger,package_name='mypackage')
    loaded_data = conf.get_data()

Multiple locations

::

    from json_config import JsonConfig
    conf = JsonConfig.new_conf(logger=self.logger,package_name='mypackage')
    conf.add_sym_name('package')
    conf.add_search_path(paths.get_data_path(file_name='conf.json', package_name='tests'))
    loaded_data = conf.get_data()


