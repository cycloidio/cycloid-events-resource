#!/usr/bin/env python3

import simplejson as json
import requests
import logging as log
import os
import sys


class EventsResource:
    """
        Events resource implementation.
        This python script is the target of symbolic links and is used for check, in and out.
        These three commands are defined as methods on this class and common parameters live in the constructor.
        To enable the debug output, the resource source configuration must have the debug parameter.
    """

    def __init__(self, command_name, json_data, command_argument):
        self.command_name = command_name
        self.command_argument = command_argument
        # Namespace the approval lock
        self.data = json.loads(json_data)
        self.token = None

        self.api_url = None
        self.api_login = None
        self.api_password = None
        self.organization = None
        self.icon = None
        self.message = None
        self.severity = None
        self.tags = None
        self.title = None
        self.type = None

        # allow debug logging to console for tests
        if os.getenv('RESOURCE_DEBUG', False) or self.data.get('source', {}).get('debug', False):
            log.basicConfig(level=log.DEBUG)
        stderr = log.StreamHandler()
        stderr.setLevel(log.INFO)
        log.getLogger().addHandler(stderr)

        log.debug('command: %s', command_name)
        log.debug('input: %s', self.data)
        log.debug('args: %s', command_argument)
        log.debug('environment: %s', os.environ)


    def check_cmd(self, source, version):
        """
        Check for new version(s)

        #TODO this first release of the resource won't check for new events/won't trigger
        But in a future version, we may want to check/filter specific events to trigger the pipeline
        https://github.com/cycloidio/cycloid-events-resource/issues/2

        :param source: is an arbitrary JSON object which specifies the location of the resource,
        including any credentials. This is passed verbatim from the pipeline configuration.
        :param version: is a JSON object with string fields, used to uniquely identify an instance of the resource.
        :return: a dict with the version fetched
        """

        log.debug('version: %s', version)

        versions_list = []
        if not version:
            version = {"timestamp": '0'}

        log.debug('source: %s', source)
        log.debug('version: %s', version)

        versions_list.append(version)
        log.debug(versions_list)

        return versions_list


    def in_cmd(self, target_dir, source, version, params):
        """
        Get an event from Cycloid API

        This first release of the resource won't get an event, we don't have usecase right now

        :param target_dir: a temporary directory which will be exposed as an output
        :param source: is the same value as passed to check
        :param version: is the same type of value passed to check, and specifies the version to fetch.
        :param params: is an arbitrary JSON object passed along verbatim from params on a get.
        :return: a dict with the version fetched and the metadata
        """
        log.debug('source: %s', source)
        log.debug('version: %s', version)
        log.debug('target_dir: %s', target_dir)
        log.debug('params: %s', params)

        if not version:
            version = {'timestamp': '0'}

        metadata = []

        metadata_path = os.path.join(target_dir, 'metadata')
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file)

        return {
            'version': version,
            'metadata': metadata,
        }

    def out_cmd(self, target_dir, source, params):
        """
        Send an event to Cycloid API

        This function will herit the parameters declared into resource source section, and override them with the params
        specified when using the PUT.

        :param target_dir:
        :param source: is the same value as passed to check.
        :param params: is an arbitrary JSON object passed along verbatim from params on a put.
        :return: a dict with the version fetched and the metadata
        """

        log.debug('target_dir: %s', target_dir)
        log.debug('source: %s', source)
        log.debug('params: %s', params)

        merge = self._merge_source_params(source, params)
        self._check_params('icon', merge)
        self._check_params('message', merge)
        self._check_params('severity', merge)
        self._check_params('title', merge)
        self._check_params('type', merge)
        self._check_params('tags', merge)

        self._send_events()

        metadata = []

        metadata_path = os.path.join(target_dir, 'metadata')
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file)

        return {
            'version': {'timestamp': '0'},
            'metadata': metadata,
        }

    def _merge_source_params(self, source, params):
        merge = source.copy()
        merge.update(params)

        return merge

    def _check_params(self, name, location):
        if name not in location:
            log.error("%s must exist in the configuration" % name)
            exit(1)
        else:
            setattr(self, name, location.get(name))

    def _send_events(self):
        payload = {
            'icon': self.icon,
            'message': self.message,
            'severity': self.severity,
            'tags': self.tags,
            'title': self.title,
            'type': self.type
        }
        headers = {
            'content-type': 'application/vnd.cycloid.io.v1+json',
            'Authorization':'Bearer %s' % self.token
        }

        r = requests.post('%s/organizations/%s/events' % (self.api_url, self.organization), data=json.dumps(payload), headers=headers)
        log.debug(r.text)


    def _login(self):
        # Login with informations
        payload = {'email': self.api_login, 'password': self.api_password}
        headers = {'content-type': 'application/vnd.cycloid.io.v1+json'}

        try:
            r = requests.post('%s/user/login' % (self.api_url), data=json.dumps(payload), headers=headers)
            self.token = r.json().get('data').get('token')
        except:
            log.error("There is an error on login, please check your configuration")
            exit(1)

    def run(self):
        """Parse input/arguments, perform requested command return output."""
        # Extract informations from the json
        source = self.data.get('source', {})
        params = self.data.get('params', {})
        version = self.data.get('version', {})


        # Ensure we are receiving the required parameters on the configuration
        self._check_params('api_url', source)
        self._check_params('api_login', source)
        self._check_params('api_password', source)
        self._check_params('organization', source)

        self._login()

        # Define which operation to perform
        if self.command_name == 'check':
            response = self.check_cmd(source, version)
        elif self.command_name == 'in':
            response = self.in_cmd(self.command_argument[0], source, version, params)
        else:
            response = self.out_cmd(self.command_argument[0], source, params)

        return json.dumps(response)

if __name__ == "__main__":
    print(EventsResource(command_name=os.path.basename(__file__),
                           json_data=sys.stdin.read(),
                           command_argument=sys.argv[1:]).run())
