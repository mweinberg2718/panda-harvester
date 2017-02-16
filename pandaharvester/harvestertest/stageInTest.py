import sys

queueName = sys.argv[1]

from pandaharvester.harvestercore.queue_config_mapper import QueueConfigMapper

queueConfigMapper = QueueConfigMapper()

queueConfig = queueConfigMapper.get_queue(queueName)

import os
import uuid
import random
import string
from pandaharvester.harvestercore.job_spec import JobSpec

jobSpec = JobSpec()
jobSpec.jobParams = {'inFiles': 'DAOD_STDM4.09596175._000008.pool.root.1',
                     'scopeIn': 'mc15_13TeV',
                     'fsize': '658906675',
                     'GUID': '7e3776f9bb0af341b03e59d3de895a13',
                     'checksum': 'ad:3734bdd9',
                     'ddmEndPointIn': 'BNL-OSG2_DATADISK',
                     'realDatasetsIn': 'mc15_13TeV.363638.MGPy8EG_N30NLO_Wmunu_Ht500_700_BFilter.merge.DAOD_STDM4.e4944_s2726_r7772_r7676_p2842_tid09596175_00',
                     }

from pandaharvester.harvestercore.plugin_factory import PluginFactory

pluginFactory = PluginFactory()

# get plugin
preparatorCore = pluginFactory.get_plugin(queueConfig.preparator)
print "plugin={0}".format(preparatorCore.__class__.__name__)

print "testing preparation"
tmpStat, tmpOut = preparatorCore.trigger_preparation(jobSpec)
if tmpStat:
    print " OK"
else:
    print " NG {0}".format(tmpOut)

print

print "testing status check"
while True:
    tmpStat, tmpOut = preparatorCore.check_status(jobSpec)
    if tmpStat == True:
        print " OK"
        break
    elif tmpStat == False:
        print " NG {0}".format(tmpOut)
        sys.exit(1)
    else:
        print " still running. sleep 1 min"
        time.sleep(60)

print

print "checking path resolution"
tmpStat, tmpOut = preparatorCore.resolve_input_paths(jobSpec)
if tmpStat:
    print " OK {0}".format(jobSpec.jobParams['inFilePaths'])
else:
    print " NG {0}".format(tmpOut)
