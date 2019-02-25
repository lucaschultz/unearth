import sys
sys.path.append('/Users/luca/GitHub/unearth/artifacts/')

from serial_number import fact as getserial
import macmodelshelf

factoid = 'model'

def fact():
    serial = getserial()
    serial = serial['serial_number']
    
    identifier = macmodelshelf.model_code(serial)
    model_raw = macmodelshelf.model(identifier)
    
    if model_raw is not None:
        model, rest = model_raw.split('(')
        model = model.rstrip()
        return {factoid: model}
    else:
        model = 'N/A'
        return {factoid: model}
        
if __name__ == '__main__':
    print '<result>%s</result>' % fact()[factoid]