if [ -z "$2" ]
then
	masses="80 90 100 110 120 130 140 150 170 180 190 210 220 230 240 300"
else
	masses="$2"
fi

for mass in $masses
do
	echo "======= Running datacard_RPVStopStopToJets_UDD312_M-${mass}_${1}"

	if [ -z "$3" ]
	then
		combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_${1}_bins.txt -n UDD312RPVSt_M-${mass}_${1}
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v05_bins.txt -n UDD312RPVSt_M-${mass}_v05_bins
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_altBkg_NOSys_v05p3_bins.txt -n UDD312RPVSt_M-${mass}_altBkg_NOSys_v05p3_bins -S 0
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_altBkg_Bin5_v05p3_bins.txt -n UDD312RPVSt_M-${mass}_altBkg_Bin5_v05p3 
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_Bin1_v05p4_bins.txt -n UDD312RPVSt_M-${mass}_altBkg_Bin5_v05p4 
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_Bin5_v05p3.txt -n UDD312RPVSt_M-${mass}_v05p3_Bin5
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v05p2.txt -n UDD312RPVSt_M-${mass}_v05p2_withPoissonBin10
		#combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v05p2_GaussShape.txt -n UDD312RPVSt_M-${mass}_v05p2_withPoissonBin10GaussShape
		#combine -M MarkovChainMC Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v05.txt -n UDD312RPVSt_M-${mass}_v05 --tries 1000
		#combine -M ProfileLikelihood Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v05.txt -n UDD312RPVSt_M-${mass}_v05 -t 1000
		#combine -M ProfileLikelihood -t 500 Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_v04.txt -n UDD312RPVSt_M-${mass} 
	else
		for ((i=0;i<=$3;i++)); do
			echo "+++++++ Running pseudoExperiment "${i}
			combine -M Asymptotic Datacards/datacard_RPVStopStopToJets_UDD312_M-${mass}_altBkg_signalInjectionTest${i}_Bin5_v05p3_bins.txt -n UDD312RPVSt_M-${mass}_altBkg_signalInjectionTest${i}_Bin5_v05p3 
		done
	fi
done
