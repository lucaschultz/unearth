#!/usr/bin/python

import subprocess
import plistlib

factoid = 'drive_capacity'

def fact():
    '''Returns the boot drive capacity'''
    result = 'None'

    try:
        proc = subprocess.Popen(
                ['/usr/sbin/diskutil', 'info', '-plist', '/'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )
        stdout, _ = proc.communicate()
    except (IOError, OSError):
        stdout = None

    if stdout:
        d = plistlib.readPlistFromString(stdout.strip())
        result = round(float(d['TotalSize']) / 10**9, 2)

    return {factoid: result}


if __name__ == '__main__':
    print '<result>%s</result>' % fact()[factoid]