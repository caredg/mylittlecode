# set up the nomachine connection to localhost:2000
set wherefrom = $1
set myverb = $2

if ($wherefrom == "CERN") then
#from inside CERN
ssh $myverb -S none -D 1080 -L 2000:cmsnx2:22 -N cmsusrslc50.cern.ch
#ssh $myverb -S none -D 1080 -L 2000:cmsnx2:22 -N cmsusr1.cern.ch
else if ($wherefrom == "OUT") then
#from outside CERN
ssh $myverb -S none -A -X -Y -C -L 1080:localhost:1081 -L 2000:localhost:2000 ecarrera@lxplus5.cern.ch ssh -v -S none -D 1081 -L 2000:cmsnx2:22 -N ecarrera@cmsusr1.cern.ch
else if ($wherefrom == "terrier") then
ssh $myverb -S none -A -X -Y -C -L 1081:localhost:1082 -L 2002:localhost:2002 ecarrera@lxplus.cern.ch ssh -v -S none -D 1082 -L 2002:bostonterrier.cern.ch:22 -N ecarrera@bostonterrier.cern.ch
else if ($wherefrom == "terrierfast") then
ssh -o GSSAPIAuthentication=no -v -S none -A -X -Y -C -L 1081:localhost:1082 -L 2015:localhost:2015 ecarrera@lxplus.cern.ch ssh -v -S none -D 1082 -L 2015:bostonterrier.cern.ch:22 -N ecarrera@bostonterrier.cern.ch

else
echo "Usage: source nomachine_connect.csh <CERN or OUT or terrier> <options>"
echo "Options: -v: verbose"
echo "NOTE: start the nomachine client to localhost:2000"
echo "NOTE2: Keep the window session open"
endif

