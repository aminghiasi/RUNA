# Instructions to generate SIM Moriond17 samples 13TeV 


This branch of the code it is only to simulate lhe/gridpacks to SIM files. 

## To run the code

Go to RUNA/RUNSimulation/test/
There you have a file called `createJobs_CRAB.sh`. This script can generate SIM files for RPV Stops from gridpacks (stored in cvmfs public areas) or lhe files stored in EOS. Initially it is hardcoded for hadronic RPV stops but it can be easily modified for other models.

Some basic instuctions:
1. To run gridpacks: 
```
./createJobs_CRAB.sh gridpacks (total number of events generated) (mass of stops) 
```
To run lhe files, first modify line 31 of `createJobs_CRAB.sh`. This file *HAS TO BE STORED* in an EOS area. Do not add the entire eos path, but just after your user name. You should also modify line 28 with a proper name of your model. After that:
```
./createJobs_CRAB.sh LHE (total number of events generated)
```

2. The previous script will create a folder with the python script needed. I will strongly recommend to run a test local job. For instance:
```
cd RPVStopStopToJets_UDD323_M-180/
cmsRun step0_RPVStopStopToJets_UDD323_M-180_gridpack_GEN_SIM.py
```

3. Once you test your job locally, you can submit it to crab by using the other python file. For instance:
```
crab submit crab3_RPVStopStopToJets_UDD323_M-180_GENSIM_step0.py
```

Once you generate these files, you should move to CMSSW_8_0_20. Following instructions in the [[README][https://github.com/RutgersHEX/RUNA/tree/v8020/RUNSimulation]] of branch v8020.


Enjoy it!. 


**DISCLAIMER**
This instructions are, by NO MEANS, any official prescription to generate events in CMS. 
Use it at your own risk!
