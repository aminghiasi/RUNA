#! /bin/bash

# If you have additional custom enhancements to your shell 
# environment, you may need to add them here

export CUR_DIR=$PWD

export SCRAM_ARCH="slc6_amd64_gcc493"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source /cms/base/cmssoft/cmsset_default.sh

# Change to your CMSSW software version
# Shown for c shell
# Also change 'username' to your username
cd /cms/gomez/Substructure/CMSSW_7_6_3_patch2/src/
eval `scramv1 runtime -sh`
date

# Switch to your working directory below
cd  $CUR_DIR

python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s DATA -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 170 -s DATA -r high -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s QCDPtAll -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s TTJets -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s WJetsToQQ -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s ZJetsToQQ -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s ZZTo4Q -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s WWTo4Q -r low -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 100 -s WZ -r low -g pruned 

#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m 190 -s QCDPtAll -r high -g pruned 
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m110 -s QCDPtAll -r low -g softDropPuppi
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m190 -s QCDPtAll -r high -g softDropPuppi
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m110 -s QCDPtAll -r low -g softDrop
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m110 -s QCDPtAll -r low -g prunedPuppi
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m190 -s QCDPtAll -r high -g softDrop
#python RUNMiniBoostedAnalyzer_HEXFARM.py -b True -m190 -s QCDPtAll -r high -g prunedPuppi
