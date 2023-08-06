"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.mockmongotestcase import get_test_case_cls_default
from heaserver.person import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import ActionSpec

db_store = {
    service.MONGODB_PERSON_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invited': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.person.Person',
        'version': None,
        'first_name': 'rex',
        'last_name:': 'textmus',
        'title': 'Doctor',
        'email': 'donotcontact@gmail.com'
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus',
            'invited': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [],
            'source': None,
            'type': 'heaobject.person.Person',
            'version': None
        }]}

TestCase = get_test_case_cls_default(coll=service.MONGODB_PERSON_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/people/',
                                     fixtures=db_store,
                                     get_actions=[ActionSpec(name='heaserver-people-person-get-properties',
                                                             rel=['properties']),
                                                  ActionSpec(name='heaserver-people-person-open',
                                                             url='/people/{id}/opener',
                                                             rel=['opener']),
                                                  ActionSpec(name='heaserver-people-person-duplicate',
                                                             url='/people/{id}/duplicator',
                                                             rel=['duplicator'])
                                                  ],
                                     get_all_actions=[ActionSpec(name='heaserver-people-person-get-properties',
                                                             rel=['properties']),
                                                      ActionSpec(name='heaserver-people-person-open',
                                                                 url='/people/{id}/opener',
                                                                 rel=['opener']),
                                                      ActionSpec(name='heaserver-people-person-duplicate',
                                                                 url='/people/{id}/duplicator',
                                                                 rel=['duplicator'])],
                                     duplicate_action_name='heaserver-people-person-duplicate-form')
