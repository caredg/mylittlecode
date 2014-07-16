#! /bin/bash --noprofile

# Script to rm files safely



# Back to basics in 2013-08-2.  It needs to be simpler.
# Just create a trash dir in, for example, 
# /tmp/ecarrera/ and dump everything there. 

# Improved by Edgar Carrera 2007-07-05
# It is now possible to rm any file from anywhere,
# it will make a mytrash directory in the area from
# where the file is gonna be removed, and it will
# move the file in there with a time stamp


# Originally thought and created by Alexey Atramentov

#first dir option
mydir="/home/ecarrera/.local/share/Trash/files"
echo $mydir
#alternative dir option (this is not working)
mydir2="~/."


#loop over files to delete
for infile in $* ; do
    if [ -e $infile ]; then
        #try to write first in the default trash dir
        # and then in home area
        if [ -d ${mydir} ]; then
            dirfile=${mydir}
        else
            if [ -d ${mydir2} ]; then
                echo "Directory \'mytrash\' is in ${mydir2}/"
                dirfile=${mydir2}
                mkdir -p ${dirfile}/mytrash
            else
                echo 'Could not create a mytrash directory'
            fi
                
        fi
          
        #Move file to mytrash directory
        barefile=`basename ${infile}`
        mv ${infile} ${dirfile}/${barefile}.removed_at_`date +%Y:%m:%d:%I:%M:%S`
        echo "File ${infile} moved to ${dirfile}/${barefile}.removed_at_`date +%Y:%m:%d:%I:%M:%S`"
        echo "Size of ${dirfile}/ = `du -sh ${dirfile}/.|awk '{print $1}'`"
    else
            echo "File $infile doesn't exist, no action has been taken..."
    fi
done




