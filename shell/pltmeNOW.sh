#!/bin/bash

BRILPRO="brilpro"
HOSTNET=`hostname -A`
echo "BRILPRO user is called " $BRILPRO
echo "You are currently in host: " $HOSTNAME
echo "You are logged in as: " $USER

#things to to do if you are already in a pltvme machine
if [[ "$HOSTNAME" =~ "vmepc" ]];then 
    echo "You are in a pltvme machine called $HOSTNAME"
    echo "You are logged in as " $USER
    if [[ $USER == $BRILPRO ]]; then
        cd /brilpro/plt/cmsplt
        echo "You are now in $PWD ..."
        echo "source setenv-prod.sh ..."
        source setenv-prod.sh
        cd interface
        echo "You are now in $PWD"
        if [[ "$PWD" =~ "/brilpro/plt/cmsplt/interface" ]];then
            echo "$(tput setaf 1) Congratulations you are now set to drive the PLT system. Remember that you are in a child shell ..."    
        fi    
        #Leave me within the child shell (in the directory I need):
        bash
    else 
        echo "Making you brilpro ..."
        xsudo -u brilpro -H bash -l
    fi
#check to see if you are in a cmsusr machine otherwise login
elif [[ "$HOSTNAME" =~ "kvm" ]];then
    echo "You are in a cmsusr machine called $HOSTNAME"
    echo "You are logged in as " $USER
    echo "Signing in pltvme1 machine ..."
    ssh -Y pltvme1
#check if you are in a machine inside the CERN network
elif [[ "$HOSTNET" =~ "cern.ch" ]];then
    echo "It looks like you are inside CERN ..."
    echo "Signing in a cmsusr machine ..."
    ssh -Y ecarrera@cmsusr
#check if you are in a machine outside the CERN network
else 
    echo "Looks like you are outside the CERN network ..."
    echo "Tunneling through lxplus to a cmsusr machine ..."
    ssh -tXY ecarrera@lxplus.cern.ch ssh -XY ecarrera@cmsusr.cern.ch
fi    
      
    