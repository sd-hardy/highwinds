#!/usr/bin/python

#Copyright: (c) 2022, Skyler Hardy <skyler.hardy@protonmail.com.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""This module is used by the Highwinds CDN modules as part of the Highwinds
ansible collection.

To use this module, include it as part of a custom module as shown below:

  from ansible_collections.sd_hardy.highwinds.plugins.module_utils.striketracker_api import ApiClient
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from json import JSONEncoder, JSONDecodeError
from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
#from ansible_collections.sd_hardy.logtail.plugins.module_utils.logtail_source import LogtailSource


class ApiError(Exception):
    def __init__(self, msg):
        self.msg = msg

class IpList:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): return {'list'}
    def to_dict(self): return dict(list=self.list)

class Platform:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','code','name','capabilities','type','available'}
    def to_dict(self):
        return dict(
                id=self.id,
                code=self.code,
                name=self.name,
                capabilities=self.capabilities,
                type=self.type,
                available=self.available,
                )

class Notification:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','createdDate','services','subject','subtitle'}
    def to_dict(self):
        return dict(
                id=self.id,
                createdDate=self.createdDate,
                services=self.services,
                subject=self.subject,
                subtitle=self.subtitle,
                )

class Doc:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'code','category','description'}
    def to_dict(self):
        return dict(
                code=self.code,
                categoy=self.category,
                description=self.description,
                )

class BillingRegion:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','code','name'}
    def to_dict(self):
        return dict(
                id=self.id,
                code=self.code,
                name=self.name,
                )

class Certificate:
    # The API does not always return these values
    optional_attrs = ['ciphers','key','certificate']
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','commonName','caBundle','domains','fingerprint','issuer',
                'requester','createdDate','updatedDate','expirationDate','trusted',
                'certificateInformation'}
    def to_dict(self):
        d = dict(
                id=self.id,
                commonName=self.commonName,
                caBundle=self.caBundle,
                domains=self.domains,
                fingerprint=self.fingerprint,
                issuer=self.issuer,
                requester=self.requester,
                createdDate=self.createdDate,
                updatedDate=self.updatedDate,
                expirationDate=self.expirationDate,
                trusted=self.trusted,
                certificateInformation=self.certificateInformation,
                )
        # Handle 'Optional' attributes (in API)
        for a in [at for at in self.optional_attrs if hasattr(self, at)]:
            d[a] = getattr(self, a)
        return d

class Pop:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','code','name','group','region','country',
                'latitude','scannable','longitude','analyzable'}
    def to_dict(self):
        return dict(
                id=self.id,
                code=self.code,
                name=self.name,
                group=self.group,
                region=self.region,
                country=self.country,
                latitude=self.latitude,
                scannable=self.scannable,
                longitude=self.longitude,
                analyzable=self.analyzable
                )

class Scope:
    # The API does not always return these values
    optional_attrs = ['name']

    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)

    def _get_attrs(self=None): return {'id','platform','path','createdDate','updatedDate'}

    def to_dict(self):
        d = dict(
                id=self.id,
                platform=self.platform,
                path=self.path,
                createdDate=self.createdDate,
                updatedDate=self.updatedDate
                )
        # Handle 'Optional' attributes (in API)
        for a in [at for at in self.optional_attrs if hasattr(self, at)]:
            d[a] = getattr(self, a)
        return d

class ScopeContainer:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): return {'scope'}
    def to_dict(self): 
        return self.scope.to_dict()

class Service:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): return {'id','name','description','type'}
    def to_dict(self):
        return dict(
                id=self.id,
                name=self.name,
                description=self.description,
                type=self.type
                )

class Origin:
    optional_attrs = [
        'id','type','createdDate','updatedDate','requestTimeoutSeconds',
        'errorCacheTTLSeconds','maxRetryCount','authenticationType', 
        'securePort','originPullHeaders','originCacheHeaders',
        'verifyCertificate','certificateCN' 
        ]

    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)
    def _get_attrs(self=None): 
        return {'id','name','type','path','createdDate','updatedDate',
                'requestTimeoutSeconds','errorCacheTTLSeconds','maxRetryCount',
                'authenticationType','hostname','port','securePort',
                'originPullHeaders','originCacheHeaders','verifyCertificate',
                'certificateCN'}
    def to_dict(self):
        d = dict(
                name=self.name,
                port=self.port,
                path=self.path,
                hostname=self.hostname,
                )
        for a in [at for at in self.optional_attrs if hasattr(self, at)]:
            d[a] = getattr(self, a)
        return d
    def requires_update(self,params):        
        diff = dict()
        for key,param in params.items():
            if hasattr(self, key):
                if param != getattr(self,key):
                    diff[key] = param
        return diff
    def format_payload(self,updates=None):
        crnt = self.to_dict()
        strip_keys = ['id','createdDate','updatedDate']
        payload = dict([(key, val) for key, val in
                    crnt.items() if key not in strip_keys])
        if updates is not None:
            for key,val in updates.items():
                payload[key] = val
        return payload 

class Host:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)

    def _get_attrs(self=None): return {'name','hashCode','type','services','scopes','createdDate','updatedDate'}
    def to_dict(self):
        return dict(
                name=self.name,
                hashCode=self.hashCode,
                type=self.type,
                createdDate=self.createdDate,
                updatedDate=self.updatedDate,
                scopes=list(scope.to_dict() for scope in self.scopes),
                services=list(service.to_dict() for service in self.services),
                )
    def to_json(self):
        return json.dumps(self, cls=Encoder)

class List:
    def __init__(self, d=None):
        if d is not None:
            for k,v in d.items():
                setattr(self, k, v)

    def _get_attrs(self=None): return {'list'}
    def to_dict(self): 
        return list(i.to_dict() for i in self.list)

class JsonHandler(JSONEncoder):
    def default(self, i): return i.__dict__

    def find_class(json_dict):
        keys = json_dict.keys()
        if keys >= Service._get_attrs():
            return Service(json_dict)
        elif keys >= Scope._get_attrs():
            if json_dict['platform'] in ['CDS','ALL']:
                return Scope(json_dict)
        elif keys >= Host._get_attrs():
            return Host(json_dict)
        elif keys >= Origin._get_attrs():
            return Origin(json_dict)
        elif keys >= Pop._get_attrs():
            return Pop(json_dict)
        elif keys >= Platform._get_attrs():
            return Platform(json_dict)
        elif keys >= Notification._get_attrs():
            return Notification(json_dict)
        elif keys >= Doc._get_attrs():
            return Doc(json_dict)
        elif keys >= Certificate._get_attrs():
            return Certificate(json_dict)
        if keys >= BillingRegion._get_attrs():
            return BillingRegion(json_dict)
        elif keys >= ScopeContainer._get_attrs():
            return ScopeContainer(json_dict)
        elif 'list' in json_dict:
            # Handle IP list response
            if len(json_dict['list']):
                if type(json_dict['list'][0]) is str:
                    return IpList(json_dict)
            return List(json_dict)

        #print('No json decoder for dict', json_dict)
        return json_dict

class ApiClient:

    def __init__(self,username=None,password=None,token=None,account=None):
        self.account = account
        self.baseurl = 'https://striketracker.highwinds.com'
        self.apiurl = self.baseurl+'/api/v1/accounts/'+self.account
        self.agent = "ansible-highwinds (Python-urllib/3.8)"
        self.headers = {'X-Application-Id': self.agent,'Accept': 'application/json, text/plain, * / *'}
        self.token = token
        if not self.token:
            self._get_token(username,password)

    def _is_json(self,data):        
        try:
            jso = json.loads(data)
        except (TypeError, ValueError) as e:
            return False
        return True

    def _to_json(self,data):
        try:
            js = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise ApiError("Unable to convert payload to JSON. Payload: %s" % payload)
        return js

    def _format_payload(self, data):
        params = list()
        for key, val in data.items():
            if val is not None:
                params.append('='.join([key, str(val)]))
        return '&'.join(params).encode()

    def _build_params(self,params):
        if len(params) == 1:
            items = params.items()
            #print('items:',items[1])

    def _get_token(self, username, password):
        """ Get an OAuth2 token using the provided credentials """
        if not username and not password:
            raise StrikeTrackerApiError(
                "You must provide an API Token or a "
                "Username and Password to authenticate"
            )
        result = self.request(            
            'POST', 
            self.baseurl + '/auth/token',
            self._format_payload(
                dict(
                    grant_type='password',
                    username=username,
                    password=password
                )
            ),
        )
        if not result:
            return False
        try:
            response = json.loads(result)
        except JSONDecodeError as e:
            raise ApiError(
                "Unable to decode API response."
                "Reason: %s. %s %s"
                % (e.msg, e.doc, e.pos)
            )
        self.token = response['access_token']
        self.headers['Authorization'] = "Bearer %s" % self.token

    def request(self, method='GET', url=None, data=None):
        """ Make a request to the StrikeTracker API """
        try:
            r = open_url(
                url,
                method=method,
                data=data,
                headers=self.headers,
                http_agent=self.agent)
            return r.read()
        except HTTPError as e:
            if e.code == 404:
                return None
            else:
                response = e.read()
                if self._is_json(response):
                    response = json.loads(response)
                errmsg = "Unable to complete API request. URL: %s, Status: %i, Reason: %s" % (url, e.code, e.reason)
                if type(response) is dict: 
                    if 'error' in response and response['error']:
                        errmsg += ", Error: %s" % response['error']
                raise ApiError(errmsg)
      
    def origins(self,method='GET',origin_id=None,config=None):
        """ Handle the origin resource """
        result,url = None,self.apiurl + '/origins'
        if origin_id is not None:
            url += '/' + str(origin_id)        
        if method in ['POST','PUT']:
            self.headers['Content-Type'] = 'application/json'            
            if not self._is_json(config):
                config = self._to_json(config)
        response = self.request(method, url, config)
        if not response:
            return None
        
        try:
            return json.loads(response, object_hook=JsonHandler.find_class)
        except JSONDecodeError as e:
            raise ApiError(
                "Unable to decode API response."
                "Reason: %s. %s %s"
                % (e.msg, e.doc, e.pos))
