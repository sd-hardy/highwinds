#!/usr/bin/python

# Copyright: (c) 2022, Skyler Hardy <skyler.hardy@protonmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: highwinds_origin

short_description: highwinds_origin

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "2.12.0"

description: A module to manage Highwinds CDN Origins.

options:
    token:
        description: Your Highwinds permanent API Token.
        required: false
        type: str
    login_user:
        description: Your Highwinds account username.
        required: false
        type: str
    login_pass:
        description: Your Highwinds account password.
        required: false
        type: str
    account:
        description: The hash ID for your Highwinds account.
        required: true
        type: str
    id:
        description: The ID of the Highwinds Origin.
        required: false
        type: int
    name:
        description: The name of the Highwinds Origin.
        required: false
        type: str
    hostname:
        description: The hostname of the Origin.
        required: false
        type: str
    port:
        description: The port to use for the Origin.
        required: false
        type: int
    securePort:
        description: The SSL enabled port to use for the Origin.
        required: false
        type: int
    type:
        description: The origin's type (defaults to EXTERNAL for external origins)
        required: false
        type: str
    path:
        description: The path to prepend requests
        required: false
        type: str
    requestTimeoutSeconds:
        description: The time before the request times out, in seconds.
        required: false
        type: int
    errorCacheTTLSeconds:
        description: Time in seconds to cache errors.
        required: false
        type: int
    maximumOriginPullSeconds:
        description: Time in seconds in which we give up attempting to pull an asset
        required: false
        type: int
    maxRequestsPerConnection:
        description: The maximum Requests Per Connection
        required: false
        type: int
    maxConnectionsPerEdge:
        description: If enabled, the maximum number of concurrent connection any single edge will make to the origin
        required: false
        type: int
    maxConnectionsPerEdgeEnabled:
        description: Indicates if the CDN should limit the number of connections each edge should make when pulling content
        required: false
        type: boolean
    maxRetryCount:
        description: How many times we attempt to pull the asset before giving up
        required: false
        type: int
    authenticationType:
        description: The authentication type to use for origin requests
        required: false
        type: str
        choices:
        - NONE
        - BASIC
    username:
        description: The username for basic authentication
        required: false
        type: str
    password:
        description: The password for basic authentication
        required: false
        type: str
    originPullHeaders:
        description: Headers to add when pulling from this origin
        required: false
        type: str
    originCacheHeaders:
        description: Headers to preserve in cached responses
        required: false
        type: str
    verifyCertificate:
        description: If we should verify the Origins SSL certificate.
        required: false
        type: boolean
    certificateCN:
        description: The certificate common name.
        required: false
        type: str
    state:
        description: State of the Highwinds Origin.
        required: false
        default: present
        type: str
        choices:
        - present
        - absent
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
#extends_documentation_fragment:
#    - sd_hardy.highwinds.my_doc_fragment_name
author:
    - Skyler Hardy (https://github.com/sd-hardy)
'''

EXAMPLES = r'''
# Create a new origin
- name: Create a Highwinds origin
  sd_hardy.highwinds.highwinds_origin:
    token: "{{ highwinds_api_token }}"
    name: MyOrigin1
    path: '/'
    port: 80
    securePort: 443
    hostname: origin1.exmaple.com
    verifyCertificate: true
    requestTimeoutSeconds: 35
    errorCacheTTLSeconds: 5
    maxRetryCount: 3
    originPullHeaders: Host: example.com
    originCacheHeaders: Access-Control-Allow-Origin,Content-Disposition
  register: create

# Print out new origin details
- name: Debug create origin
  debug:
    var: create

# Update our origins path
- name: Update origin
  sd_hardy.highwinds.highwinds_origin:
    token: "{{ highwinds_api_token }}"
    id: "{{ my_origin1.id }}"
    name: MyOrigin1
    path: '/my/content'
    port: 80

# Delete an origin
- name: Delete origin
  sd_hardy.highwinds.highwinds_origin:
    token: "{{ highwinds_api_token }}"
    id: "{{ my_origin1.id }}"
    state: absent
'''

RETURN = r'''
# These are examples of possible return values:
action:
    description: Describes the action taken against the API
    type: str
    returned: always
    sample: 'updated'
origin:
    description: Dictionary containing the Origin.
    returned: On success
    type: complex
    contains:
        id:
            description: The Origin ID.
            type: str
            sample: 123456
        name:
            description: The Orign name.
            type: str
            sample: "My Origin 01"
        type:
            description: Highwinds Origin Type. This defaults to 'EXTERNAL'.
            type: str
            sample: "EXTERNAL"
        path:
            description: The path to prepend to requests
            type: str
            sample: "/path/to/content"
        createdDate:
            description: Timestamp when created
            type: str
            sample: "2020-01-01 13:01:20"
        updatedDate:
            description: Timestamp when updated
            type: str
            sample: "2020-01-01 13:01:20"
        requestTimeoutSeconds:
            description: The time before the request times out, in seconds.
            type: int
            sample: 30
        errorCacheTTLSeconds:
            description: Time in seconds to cache errors.
            required: false
            type: int
            sample: 30
        maximumOriginPullSeconds:
            description: Time in seconds in which we give up attempting to pull an asset
            required: false
            type: int
            sample: 30
        maxRequestsPerConnection:
            description: The maximum Requests Per Connection
            required: false
            type: int
            sample: 100
        maxConnectionsPerEdge:
            description: If enabled, the maximum number of concurrent connection any single edge will make to the origin
            type: int
            sample: 50
            type: int
        maxConnectionsPerEdgeEnabled:
            description: Indicates if the CDN should limit the number of connections each edge should make when pulling content
            required: false
            type: boolean
        maxRetryCount:
            description: How many times we attempt to pull the asset before giving up
            required: false
            type: int
            sample: 5
        authenticationType:
            description: The authentication type to use for origin requests. Either NONE (default) or 'BASIC'
            required: false
            type: str
            sample: 'BASIC'
        username:
            decription: The username to use for basic authentication.
            type: str
            sample: 'my_username'
        originPullHeaders:
            description: Headers to add when pulling from this origin
            type: str
            sample: "Origin: www.example.com"
        originCacheHeaders:
            description: Comma separated list of origin headers to preserve in the cache
            type: str
            sample: "Access-Control-Allow-Origin,Content-Disposition"
        verifyCertificate:
            description: If we should verify the Origins SSL certificate.
            required: false
        certificateCN:
            description: The certificate common name to validate.
            required: false
            sample: example.com
sample:
  action: "update"
  origin: {
        "id": 123456,
        "name": "MyOrigin1",
        "type": "EXTERNAL",
        "path": "/path/to/content",
        "createdDate": "2020-01-01 13:01:20",
        "updatedDate": "2020-01-01 21:00:09",
        "requestTimeoutSeconds": 30,
        "errorCacheTTLSeconds": 120,
        "maxRetryCount": 3,
        "authenticationType": "NONE",
        "hostname": "myorigin1.example.com",
        "port": 80,
        "securePort": 443,
        "originPullHeaders": "Host: myorigin1.example.com",
        "originCacheHeaders": "Access-Control-Allow-Origin",
        "verifyCertificate": true,
        "certificateCN": "myorigin2.example.com"
  }
'''

from ansible.module_utils.basic import AnsibleModule

import json
import time
from json import JSONDecodeError
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible_collections.sd_hardy.highwinds.plugins.module_utils.striketracker_api import ApiClient, ApiError, Origin
#from ansible.highwinds.striketracker_api import ApiClient, ApiError, Origin


def run_module():
    module_args = dict(
        login_user=dict(type='str', required=False, no_log=True, aliases=['user', 'login_username']),
        login_pass=dict(type='str', required=False, no_log=True, aliases=['pass', 'login_password']),
        token=dict(type='str', required=False, no_log=True, aliases=['api_token']),
        account=dict(type='str', required=True),
        id=dict(type='int', required=False),
        name=dict(type='str', required=False),
        hostname=dict(type='str', required=False, aliases=['host']),
        port=dict(type='int', required=False),
        type=dict(type='str', required=False, default='EXTERNAL'),
        path=dict(type='str', required=False, aliases=['uri']),
        originPullHeaders=dict(type='str', required=False),
        originCacheHeaders=dict(type='str', required=False),
        certificateCN=dict(type='str', required=False),
        requestTimeoutSeconds=dict(type='int', required=False),
        errorCacheTTLSeconds=dict(type='int', required=False),
        maxRetryCount=dict(type='int', required=False),
        securePort=dict(type='int', required=False),
        maximumOriginPullSeconds=dict(type='int', required=False),
        maxRequestsPerConnection=dict(type='int', required=False),
        maxConnectionsPerEdge=dict(type='int', required=False),
        maxConnectionsPerEdgeEnabled=dict(type='bool', required=False),
        verifyCertificate=dict(type='bool', required=False),
        config=dict(type='str', required=False),
        username=dict(type='str', required=False, no_log=True, aliases=['basic_username', 'auth_username','basicAuthUser']),
        password=dict(type='str', required=False, no_log=True, aliases=['basic_password', 'auth_password', 'basicAuthPass']),
        authenticationType=dict(type='str', default='NONE', choices=['NONE', 'BASIC']),
        state=dict(type='str', default='present', choices=['present', 'absent']),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ('token', 'login_user'),
        ],
        required_one_of=[
            ('token', 'login_user'),
        ],
        required_together=[
            ('login_user', 'login_pass'),
            ('hostname', 'port', 'path')
        ],
        required_if=[
            ('state', 'absent', ['id'], True),
            ('state', 'present', ('id', 'hostname'), True)
        ],
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        action='none',
        origin=dict(),
    )
    if module._diff:
        result['diff'] = dict()

    token = module.params['token']
    login_username = module.params['login_user']
    login_password = module.params['login_pass']
    account = module.params['account']
    config = module.params['config']
    id = module.params['id']
    state = module.params['state']

    # Handle building payload
    payload = None
    if config is not None:
        payload = config
    else:
        payload = dict()
        for key, param in module.params.items():
            if (key not in ['token', 'login_user', 'login_pass',
               'account', 'config', 'id', 'state']):
                if param is not None:
                    payload[key] = param

    try:
        st = ApiClient(
            username=login_username,
            password=login_password,
            token=token,
            account=account)

        origin = None
        if id is not None:
            # Grab the origin with ID
            origin = st.origins(origin_id=id)
        if not origin and 'hostname' in payload:
            # Find the origin by hostname
            origins = st.origins()
            for o in origins.list:
                if o.hostname == payload['hostname']:
                    origin = o
                    break
        if origin is not None:
            result['origin'] = origin.to_dict()
            if module._diff:
                result['diff']['after'] = dict()
                result['diff']['before'] = origin.to_dict()
            if state == 'present':
                # Check if the origin requires update
                updates = origin.requires_update(payload)
                if updates:
                    result['changed'] = True
                    if module.check_mode:
                        if module._diff:
                            result['diff']['after'] = origin.to_dict() | updates
                        return module.exit_json(**result)
                    updated = st.origins(origin_id=origin.id,
                                         method='PUT',
                                         config=origin.format_payload(updates))
                    if updated is not None:
                        result['action'] = 'updated'
                        result['origin'] = updated.to_dict()
                        if module._diff:
                            result['diff']['after'] = updated.to_dict()
            if state == 'absent':
                result['changed'] = True
                if module.check_mode:
                    return module.exit_json(**result)
                deleted = st.origins(origin_id=origin.id, method='DELETE')
                if deleted is not None:
                    result['action'] = 'deleted'
                    result['origin'] = origin.to_dict()
            return module.exit_json(**result)
        else:
            if state == 'present' and payload is not None:
                result['changed'] = True
                if module.check_mode:
                    return module.exit_json(**result)
                created = st.origins(method='POST',
                                     config=Origin(payload).format_payload())
                if created is not None:
                    result['action'] = 'created'
                    result['origin'] = created.to_dict()
                    if module._diff:
                        result['diff']['after'] = created.to_dict()
            return module.exit_json(**result)
    except Exception as exc:
        return module.fail_json(
            msg='An error ocurred during module execution: %s' % str(exc), **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
