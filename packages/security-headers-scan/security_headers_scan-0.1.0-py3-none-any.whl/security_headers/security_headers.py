import logging
from enum import Enum
import requests
from requests.exceptions import ConnectionError
import yaml
from mimetypes import init
from functools import partial


logger = logging.getLogger('ca_security_headers')

def _exists(name, value, options):
    return bool(value)
    
def _not_exists(name, value, options):
    return not bool(value)
    
def _true(name, value, options):
    return True

def _equals(name, value, options):
    if isinstance(value, list) and not isinstance(options, list):
        options = [options]
    return value == options

def _any(name, value, options):
    if not isinstance(options, list):
        options = [options]
    if not isinstance(value, list):
        value = [value]
    intersection = [v for v in value if v in options]
    return bool(intersection)

def _all(name, value, options):
    if not isinstance(options, list):
        options = [options]
    if not isinstance(value, list):
        value = [value]
    return all(v in value for v in options)

def _none(name, value, options):
    if not isinstance(options, list):
        options = [options]
    if not isinstance(value, list):
        value = [value]
    intersection = [v for v in value if v in options]
    return not bool(intersection)

class Requirement(object):

    class Type(Enum):
        Rule = 1
        Condition = 2
    
    def __init__(self, name, verify, record_none_value=True, type=Type.Rule) -> None:
        self.name = name
        self.verify = verify
        self.record_none_value = record_none_value
        self.type = type
            

class SecurityHeaders():
    
    requirements = {
        'MUST': Requirement('MUST', _exists),
        'SHOULD': Requirement('SHOULD', _exists),
        'COULD': Requirement('COULD', _true, record_none_value=False),
        'MUST_NOT': Requirement('MUST_NOT', _not_exists),
        'SHOULD_NOT': Requirement('SHOULD_NOT', _not_exists),
        'EQ': Requirement('EQ', _equals, type=Requirement.Type.Condition),
        'ANY': Requirement('ANY', _any, type=Requirement.Type.Condition),
        'ALL': Requirement('ALL', _all, type=Requirement.Type.Condition),
        'NONE': Requirement('NONE', _none, type=Requirement.Type.Condition)
    }
    
    def _filter_requirements(policy, type):
        result = dict()
        if isinstance(policy, dict):
            for k, v in policy.items():
                requirement = SecurityHeaders.requirements[k]
                if requirement.type == type:
                    result[requirement] = v
        return result
        
    def _rule_requirements(policy):
        return SecurityHeaders._filter_requirements(policy, Requirement.Type.Rule)

    def _condition_requirements(policy):
        return SecurityHeaders._filter_requirements(policy, Requirement.Type.Condition)

    def _load_policy(policy_file):
        with open(policy_file or 'security_headers/security-headers-policy.yml') as f:
            result = yaml.safe_load(f)
            logger.info(result)
            return result
    
    def __init__(self, policy=None, policy_file=None) -> None:
        self.policy = policy or SecurityHeaders._load_policy(policy_file)
    
    def scan(self, url):
        
        def _directives(value):
            directives = dict()
            if value:
                parts = value.split(';')
                for part in parts:
                    sub_parts = part.strip().split(' ')
                    directives[sub_parts[0]] = sub_parts[1:]
            return directives
            
        def verify(policy, value_map, header_name=None):
            for rule, rule_options in SecurityHeaders._rule_requirements(policy).items():
                for name, options in rule_options.items():
                    value = value_map.get(name, None)
                    expected_value = options
                    compliant = rule.verify(name, value, options)
                    if compliant:
                        for condition, condition_options in SecurityHeaders._condition_requirements(options).items():
                            compliant = condition.verify(name, value, condition_options)
                    record = {
                        'url': url,
                        'requirement': rule.name,
                        'compliant': compliant,
                        'actual_value': value,
                        'expected_value': expected_value
                    }
                    if header_name:
                        record['header'] = header_name
                        record['directive'] = name
                    else:
                        record['header'] = name
                    logger.info(f'{record}')
                    if value or rule.record_none_value:
                        scan_records.append(record)
                    
                    # verify directives
                    if (compliant):
                        directive_policy = SecurityHeaders._rule_requirements(options)
                        if directive_policy:
                            verify(options, _directives(value), name)
                

        scan_records = []
        try:
            response = requests.head(url)
            logger.info(f'headers from [{url}]: {response.headers}')
            verify(self.policy, response.headers)
        except ConnectionError as e:
            logger.error(f'Error connecting to {url}: {e}')
        return scan_records
    
     