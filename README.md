# RU Simulations and Ntuples  

This package contains scripts:

* RUNGeneration contains a simple script to set your madgraph environment. 
* RUNSimulations generates MC samples from lhe files.

### Instructions
```
cmsrel CMSSW_7_1_25_patch1/
cd CMSSW_7_1_25_patch1/src/
cmsenv
git clone git@github.com:RutgersHEX/RUNA.git -b v7124
scram b -j 18
cmsenv
```

This branch is just to generate LHE-SIM files. 


> Disclaimer
> This is not an official CMS recipe. Use it with your own risk.
