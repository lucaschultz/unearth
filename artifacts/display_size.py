import sys
sys.path.append('/Users/luca/GitHub/unearth/artifacts/')
import re
from serial_number import fact as getserial
import macmodelshelf

factoid = 'display_size'

def fact():
    serial = getserial()
    serial = serial['serial_number']
    
    identifier = macmodelshelf.model_code(serial)
    model_raw = macmodelshelf.model(identifier)
    
    if model_raw is not None:
        model, rest = model_raw.split('(')
        list = [int(s) for s in re.findall(r'-?\d+\.?\d*', model_raw)]
        display_size = list[0]
        return {factoid: display_size}
    else:
        model = 'N/A'
        return {factoid: display_size}
        
if __name__ == '__main__':
    print '<result>%s</result>' % fact()[factoid]