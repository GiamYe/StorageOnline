__author__ = 'xiang'
# coding = utf8

import sheepdog

sd = sheepdog.SheepDog(url='http://172.16.17.201', container='testacct')

sd.create_object(file='big.vmdk', uuid='big.vmdk')

#sd.get_object(uuid='big.vmdk')