#!/bin/bash 

###########################################################################
###
###  Simple bash script to create python files for simulation.
###
###  Alejandro Gomez Espinosa
###  gomez@physics.rutgers.edu
###
###  How to run: 
###  source createJobs_CRAB.sh
###  (If it is an executable (chmod +x createJobs.sh):
###  ./createJobs_CRAB.sh 
###
###  You must change the PARAMETERS according with your needs. 
###  Initially is the only part that you should modify.
###
###########################################################################

######################################
### PARAMETERS
#####################################

stop1=${2}	## You can use this parameters later to make everything simpler. 
coupling=UDD323
totalNumberEvents=${3}

Name=RPVStopStopToJets_${coupling}_M-${stop1}_TuneCUETP8M1_13TeV-madgraph-pythia8       ##### UDD312 is for stop to jj, UDD323 for stop to bj

##### if using lhe modify this line
LHEFile=/store/user/algomez/lhe/RPVStop100_UDD323_13TeV_200k.lhe			#### DONT USE the entire eos path!!!!!



#####################################################
#### Here is where the code starts.. 
#### Initially you shouldn't modify this part
#####################################################
echo " Creating directories..."
Main_Dir=$PWD 
####### Working directory
Working_Dir=${Main_Dir}/${Name}	
if [ -d $Working_Dir ]; then
	rm -rf $Working_Dir
	mkdir -p $Working_Dir
else
	mkdir -p $Working_Dir
fi

cd $Working_Dir/

##############################################
##### Create the python file for Ntuples
##############################################

echo " Creating python file for GEN-SIM .. "
step0PythonFile="step0_${Name}_${1}_GEN_SIM.py"
cp ${Main_Dir}/step0_${1}_GEN_SIM.py  ${step0PythonFile}

########################################################
######### Small file with the commands for condor
########################################################
echo " Creating crab files .... "

crabFileStep0=crab3_${Name}_GENSIM_step0.py
cp ${Main_Dir}/crab3.py  ${crabFileStep0}
sed -i 's/NAME/'"${Name}"'/' ${crabFileStep0}
sed -i 's/test/'"${step0PythonFile}"'/' ${crabFileStep0}

if [[ ${1} == *'LHE'* ]]; then
	sed -i 's,/store/user/algomez/RPVSttojj_13TeV/RPVSt200tojj_13TeV.lhe,'"${LHEFile}"',' ${step0PythonFile}
	unitPerJob=100

elif [[ ${1} == *'gridpack'* ]]; then
	sed -i 's/HadRPVStop180_UDD323_13TeV_tarball/HadRPVStop'"${stop1}"'_'"${coupling}"'_13TeV_tarball/' ${step0PythonFile}
	unitPerJob=2000
	dummy=280
	if [ "$stop1" -gt 280 ]; then
		sed -i 's/process.generator+process.htFilter/process.generator/' ${step0PythonFile}
	fi
fi

sed -i 's/NJOBS = 1000/NJOBS = '"$((${totalNumberEvents} / ${unitPerJob}))"'/' ${crabFileStep0}
sed -i 's/unitsPerJob = 2000/unitsPerJob = '"${unitPerJob}"'/' ${crabFileStep0}


#################################
##### To make it run
#################################
echo ' To make it run: 
First load the libraries (only once per session):
source /uscmst1/prod/grid/gLite_SL5.sh
source /uscmst1/prod/grid/CRAB/crab.sh

Create and submit your jobs (Example for step0):
cd '${Name}'
crab -create -cfg '${crabFileStep0}' 
crab -submit NUMBER_JOBS -cfg '${crabFileStep0}' 

To check the status:
crab -status -c '${Name}'_GENSIM

To resubmit failed jobs:
crab -resubmit LIST_OF_FAILED_JOBS  -c '${Name}'_GENSIM 

When your jobs are done:
crab -report -c '${Name}'_GENSIM

' >> README

echo 'Crab instructions in the README file'
echo 'Have a nice day :D '

user=`echo $USER`
sed -i 's/algomez/'"${user}"'/g' *.py

