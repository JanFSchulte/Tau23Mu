import subprocess

def get_path(i, era, v, phipi=True, phimunu=False, year = 2024):

    if year == 2024:
        #if phipi: file= f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2024era{era}_v{v}_stream{i}_Mini_v1'
        if phipi: file= f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2024ReRecoera{era}_v{v}_stream{i}_Mini_v1'
        elif phimunu: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiMuNu_2024era{era}_v{v}_stream{i}_Mini_v1'
        else: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimDsTau3mu_2024ReRecoera{era}_v{v}_stream{i}'

    elif year == 2022:
        if phipi: 
            if era == "F" or era == "G": 
                file= f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2022era{era}_22Sep2023_stream{i}_PS'
            else:
                file= f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2022era{era}_10Dec2022_stream{i}_PS'
        elif phimunu: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiMuNu_2022era{era}_v{v}_stream{i}_Mini_v1'
        else: file = f'/store/user/bsimon/ParkingDoubleMuonLowMass{i}/SkimDsTau3mu_2022era{era}_v{v}_stream{i}_Mini_v1'

    elif year == 2023:
        if phipi: file= f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2022era{era}_v{v}_stream{i}_PS'
        elif phimunu: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiMuNu_2023era{era}_v{v}_stream{i}_Mini_v1'
        else: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimDsTau3mu_2022era{era}_v{v}_stream{i}_SoftMVAVars'


        
    #output = subprocess.check_output(['gfal-ls', 'davs://eos.cms.rcac.purdue.edu:9000'+file], universal_newlines=True)
    output = subprocess.check_output(['ls', '/eos/purdue/'+file], universal_newlines=True)
    print (output)
    dirs = output.split('\n')
    dirs = [item for item in dirs if item.strip()]
    print (dirs)
    output = dirs[-1]
    
    output = output.replace('\n', '')
    print (output)
    new_file = file + '/' + output
    return new_file

