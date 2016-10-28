export X509_USER_PROXY=/afs/cern.ch/user/a/algomez/x509up_u15148
cd /afs/cern.ch/work/a/algomez/RPVStops/CMSSW_7_6_3_patch2/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/work/a/algomez/RPVStops/CMSSW_7_6_3_patch2/src/RUNA/RUNAnalysis/test/
source tmp.sh RPV
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s TTJets -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s WJetsToQQ  -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s ZJetsToQQ  -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s WWTo4Q  -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s ZZTo4Q  -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s WZ  -v v05
#./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s QCDPtAll -v v05
./RUNMiniBoostedAnalyzer.py -m 100 -p single -r low -s DATA -v v05

#cmsRun simpleMatching.py
#python RUNMiniAnalyzer.py -s QCDPt
#python RUNMiniBoostedAnalyzer.py -m 100 -s DATA -r low -g pruned 
#python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g pruned 
#python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g softDropPuppi
#python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g softDropPuppi
#python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g softDrop
#python RUNMiniBoostedAnalyzer.py -m 110 -s DATA -r low -g prunedPuppi
#python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g softDrop
#python RUNMiniBoostedAnalyzer.py -m 190 -s DATA -r high -g prunedPuppi

#python RUNBkgEstimation.py -m 110 -p DATA -r low -g pruned 
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g softDrop
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g softDropPuppi
#python RUNBkgEstimation.py -m 110 -p DATA -r low -g prunedPuppi
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g softDrop
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g pruned 
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g softDropPuppi
#python RUNBkgEstimation.py -m 190 -p DATA -r high -g prunedPuppi
