from maintenance_calendar.validator.validator_factory import ValidatorFactory
from maintenance_calendar.validator.concrete_factories.json_validator_factory import JSONValidatorFactory
from maintenance_calendar.validator.concrete_factories.xml_validator_factory import XMLValidatorFactory

def get_factory(mimetype):

    ValidatorFactory.mime = mimetype
    print "entro factory", mimetype
    if 'application/json' in mimetype:
    	print "****Sale el JSONValidator"
        concrete_factory = JSONValidatorFactory()
    elif 'application/xml' in mimetype:
        concrete_factory = XMLValidatorFactory()
    else:
        concrete_factory = ValidatorFactory(mimetype)
    
    return concrete_factory