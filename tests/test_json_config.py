import unittest

import os
from os import path
import json

import standard_logger

from json_config import JsonConfig
from pyxutils import paths


class TestConfig(unittest.TestCase):

    TEST_LOGGER = None

    @classmethod
    def setUpClass(cls):
        if not cls.TEST_LOGGER:
            cls.TEST_LOGGER = standard_logger.get_logger('tests', level_str='DEBUG', console=True)
        cls.logger = cls.TEST_LOGGER

    def write_file(self, file_path, contents):
        if path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as f:
            f.write(contents)

    def find_temp_dir(self):
        temp_dir = None
        if 'TMP' in os.environ:
            if path.exists(os.environ['TMP']):
                temp_dir = os.environ['TMP']
        if not temp_dir and 'TEMP' in os.environ:
            if path.exists(os.environ['TEMP']):
                temp_dir = os.environ['TEMP']
        if not temp_dir:
            tmp_dir_home = "{0}/tmp".format(os.environ['HOME'])
            if not path.exists(tmp_dir_home):
                os.mkdir(tmp_dir_home)
            temp_dir = tmp_dir_home

        return temp_dir

    def write_file_to_tmp_dir(self, file_name, contents):
        temp_dir = self.find_temp_dir()
        file_path = path.normpath(path.join(temp_dir, file_name))
        self.write_file(file_path, contents)
        return file_path

    def test_001_load_single_config_file(self):
        self.logger.debug("TestConfig: test_001_load_single_config_file")
        # Always use an explicit new conf object
        conf = JsonConfig.new_conf(logger=self.logger,package_name='tests')

        test_conf_file_name = "config.json"
        test_data = {"key1":"value1"}
        test_config_file_contents = json.dumps(test_data)
        test_conf_file_path = self.write_file_to_tmp_dir(test_conf_file_name, test_config_file_contents)

        # Set up conf object
        conf.use_default_sym_names = False
        conf.set_conf_name(test_conf_file_name)
        conf.add_search_path(test_conf_file_path)
        conf.expand_search_paths()

        full_search_paths = conf.full_search_paths
        # Only search path should be the one we added
        self.assertEqual(test_conf_file_path,full_search_paths[0])

        loaded_data = conf.get_data()
        # Clean up
        os.remove(test_conf_file_path)
        self.assertEqual(loaded_data, test_data)

    def test_002_load_multiple_config_files(self):
        self.logger.debug("TestConfig: test_002_load_multiple_config_files")
        # Always use an explicit new conf object
        conf = JsonConfig.new_conf(logger=self.logger,package_name='tests')

        test_conf_file_name = "conf.json"
        test_data = { "key1":"val2.1", "key5":"val2.5"}
        test_config_file_contents = json.dumps(test_data)
        test_conf_file_path = self.write_file_to_tmp_dir(test_conf_file_name, test_config_file_contents)

        # Set up conf object - search paths are ordered
        conf.use_default_sym_names = False
        conf.add_sym_name('package')
        conf.add_sym_name('unknown_sym_name')
        conf.add_search_path(test_conf_file_path)
        conf.add_search_path(paths.get_data_path(file_name='conf.json', package_name='tests'))

        conf.expand_search_paths()

        full_search_paths = conf.full_search_paths
        self.assertEqual(len(full_search_paths),4)
        # Only search path that can be tested here is the test_conf_file_path
        self.assertEqual(test_conf_file_path,full_search_paths[2])

        loaded_data = conf.get_data()
        # Clean up
        os.remove(test_conf_file_path)
        self.assertEqual(loaded_data["key1"], "val3.1")
        self.assertEqual(loaded_data["key2"], "val3.2")
        self.assertEqual(loaded_data["key4"], "val1.4")
        self.assertEqual(loaded_data["key5"], "val2.5")
        self.assertEqual(loaded_data["key6"], "val3.6")

    def test_003_load_config_file_from_env(self):
        self.logger.debug("TestConfig: test_003_load_config_file_from_env")
        # Always use an explicit new conf object
        conf = JsonConfig.new_conf(logger=self.logger,package_name='tests')

        test_conf_file_name = "conf.json"
        test_data = { "key1":"val2.1", "key5":"val2.5"}
        test_config_file_contents = json.dumps(test_data)
        test_conf_file_path = self.write_file_to_tmp_dir(test_conf_file_name, test_config_file_contents)

        # Set up conf object - search paths are ordered
        conf.use_default_sym_names = False
        os.environ['JSON_CONF_DIR'] = path.dirname(test_conf_file_path)
        os.environ['JSON_CONF'] = test_conf_file_name
        conf.add_sym_name('env')
        conf.expand_search_paths()

        full_search_paths = conf.full_search_paths
        self.assertEqual(len(full_search_paths),1)
        # Only search path that can be tested here is the test_conf_file_path
        self.assertEqual(test_conf_file_path,full_search_paths[0])

        loaded_data = conf.get_data()
        # Clean up
        del os.environ['JSON_CONF_DIR']
        del os.environ['JSON_CONF']
        os.remove(test_conf_file_path)
        self.assertEqual(loaded_data["key1"], "val2.1")
        self.assertEqual(loaded_data["key5"], "val2.5")

