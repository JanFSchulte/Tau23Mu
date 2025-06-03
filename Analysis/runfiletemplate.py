import subprocess

def get_path(i, era, v, phipi=True, phimunu=False):

    if phipi: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiPi_2024era{era}_v{v}_stream{i}_Mini_v1'
    elif phimunu: file = f'/store/user/jschulte/ParkingDoubleMuonLowMass{i}/SkimPhiMuNu_2024era{era}_v{v}_stream{i}_Mini_v1'
    else: file = f'/store/user/bsimon/ParkingDoubleMuonLowMass{i}/SkimDsTau3mu_2024era{era}_v{v}_stream{i}_Mini_v1'
        
    #output = subprocess.check_output(['gfal-ls', 'davs://eos.cms.rcac.purdue.edu:9000'+file], universal_newlines=True)
    output = subprocess.check_output(['ls', '/eos/purdue/'+file], universal_newlines=True)

    dirs = output.split('\n')
    output = dirs[-1]
    
    output = output.replace('\n', '')

    new_file = file + '/' + output
    return new_file

