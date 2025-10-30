#include "myAnalizer.C"
#include "myAnalizer_control.C"
#include "myAnalizer_control_2022.C"
#include "myAnalizer_phimunu.C"
#include <TROOT.h>
#include <stdio.h>
#include <iostream>
#include <string.h>

using namespace std;

int main(int narg, char** arg){
    TTree *tree;
    char type[10];
    strcpy(type, arg[1]);
    cout << "type : " << type << endl;
    char datasetName[15];
    strcpy(datasetName, arg[2]);
    cout << "datasetName : " << datasetName << endl << endl;
    TString fileout = "";
    std::cout << "test" << std::endl;
    // Check input arguments
    if(strcmp(type, "MC") != 0 && strcmp(type, "data") != 0 && strcmp(type, "data_control") != 0 && strcmp(type, "data_control_2022") != 0 && strcmp(type, "data_phimunu") != 0 && strcmp(type, "MC_phimunu") != 0){
        cout << "The first argument is wrong! Please choose among 'MC', 'data', 'data_control'" << endl;
        //return -1;
    }
    if( strcmp(type, "MC") == 0 && (strcmp(datasetName, "DsPhiPi") != 0 && strcmp(datasetName, "DsPhiPi2022") != 0 && strcmp(datasetName, "DsPhiMuNu") != 0 && strcmp(datasetName, "Ds") != 0 && strcmp(datasetName, "Bp") != 0 && strcmp(datasetName, "B0") != 0) ){
        cout << "The second argument is wrong! Please choose between 'Ds', 'B0', 'Bp', 'DsPhiMuNu' and 'DsPhiPi'" << endl;
        return -1;
    }

    // ################ MC
    if ( strcmp(type, "MC") == 0 || strcmp(type, "MC_phimunu") == 0 ){
        cout << "This is a MC" << endl;
        
        // ###SIGNAL samples
        // Ds -> Tau -> 3Mu
        if (strcmp(datasetName, "Ds") == 0){
            cout << "MC Dataset : Ds -> Tau -> 3Mu" << endl << endl;
            TChain* chain = new TChain("TreeMakerBkg/ntuple");
        //AddFile_MCDs_tau3mu
        //OutFile_MCDs_tau3mu
        myAnalizer class_data(chain, fileout);
        class_data.Loop_Tau3mu(type, datasetName);
        }
        // Bd -> Tau -> 3Mu
        if (strcmp(datasetName, "B0") == 0){
            cout << "MC Dataset : B0 -> Tau -> 3Mu" << endl << endl;
            TChain* chain = new TChain("TreeMakerBkg/ntuple");
        //AddFile_MCB0_tau3mu
        //OutFile_MCB0_tau3mu
        myAnalizer class_data(chain, fileout);
        class_data.Loop_Tau3mu(type, datasetName);
        }
        // Bu -> Tau -> 3Mu
        if (strcmp(datasetName, "Bp") == 0){
            cout << "MC Dataset : Bp -> Tau -> 3Mu" << endl << endl;
            TChain* chain = new TChain("TreeMakerBkg/ntuple");
        //AddFile_MCBp_tau3mu
        //OutFile_MCBp_tau3mu
        myAnalizer class_data(chain, fileout);
        class_data.Loop_Tau3mu(type, datasetName);
        }
        
        // ###Other samples
        // Ds -> PhiPi -> MuMuPi
         if (strcmp(datasetName, "DsPhiPi") == 0){
            cout << "MC Dataset : Ds -> PhiPi -> MuMuPi" << endl << endl;
            TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_MCDsPhiPi_control
        //OutFile_MCDsPhiPi_control
            myAnalizer_control class_data(chain, fileout);
            class_data.Loop_DsPhiPi(type, datasetName);
         }
	 if (strcmp(datasetName, "DsPhiPi2022") == 0){
            cout << "MC Dataset : Ds -> PhiPi -> MuMuPi" << endl << endl;
            TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_MCDsPhiPi2022_control
        //OutFile_MCDsPhiPi2022_control
            myAnalizer_control_2022 class_data(chain, fileout);
            class_data.Loop_DsPhiPi(type, datasetName);
         }
 
        // Ds -> PhiMuNu -> 3MuNu
         if ((strcmp(datasetName, "DsPhiMuNu") == 0) && (strcmp(type, "MC_phimunu") ==0)){
         cout << "MC Dataset : Ds -> PhiMuNu -> 3MuNu" << endl << endl;
         TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_MCDsPhiMuNu_phimunu
        //OutFile_MCDsPhiMuNu_phimunu
        myAnalizer_phimunu class_data(chain, fileout);
        class_data.Loop_DsPhiPi(type, datasetName);
	}
         else if (strcmp(datasetName, "DsPhiMuNu") == 0){
         cout << "MC Dataset : Ds -> PhiMuNu -> 3MuNu" << endl << endl;
         TChain* chain = new TChain("TreeMakerBkg/ntuple");
        //AddFile_MCDsPhiMuNu_tau3mu
        //OutFile_MCDsPhiMuNu_tau3mu
        myAnalizer class_data(chain, fileout);
        class_data.Loop_Tau3mu(type, datasetName);
	}

   }

   //Data - tau3mu
   if(strcmp(type, "data") == 0){
	cout << "this is data" << endl;
        cout << "Data " << datasetName << endl << endl;
        TChain* chain = new TChain("TreeMakerBkg/ntuple");
        //AddFile_data_tau3mu
        //OutFile_data_tau3mu
        myAnalizer class_data(chain, fileout);
        class_data.Loop_Tau3mu(type, datasetName);
    }
    
    if (strcmp(type, "data_control") == 0){
        cout << "Control channel analysis on data" << endl;
        cout << "Data " << datasetName << endl << endl;
        TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_data_control_control
        //OutFile_data_control_control
        myAnalizer_control class_data(chain, fileout);
        class_data.Loop_DsPhiPi(type, datasetName); 
    }
    if (strcmp(type, "data_control_2022") == 0){
        cout << "Control channel analysis on data" << endl;
        cout << "Data " << datasetName << endl << endl;
        TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_data_control_2022_control
        //OutFile_data_control_2022_control
        myAnalizer_control_2022 class_data(chain, fileout);
        class_data.Loop_DsPhiPi(type, datasetName); 
    }

    if (strcmp(type, "data_phimunu") == 0){
        cout << "phimunu channel analysis on data" << endl;
        cout << "Data " << datasetName << endl << endl;
        TChain* chain = new TChain("Tree3Mu/ntuple");
        //AddFile_data_phimunu_phimunu
        //OutFile_data_phimunu_phimunu
        myAnalizer_phimunu class_data(chain, fileout);
        class_data.Loop_DsPhiPi(type, datasetName); 
    }


    return 0;
}
