#script to clean boot partition
#cleans all the old kernels except the current and
#the last one.
set current_kernel = `uname -r`
set lines = `dpkg --get-selections | grep 'linux-image' | awk '{print $1}' | egrep -v "linux-image-${current_kernel}|linux-image-generic"`
set mycount = 1
set mylimit = `echo $lines | wc | awk '{print $2}'`
while ( $mycount < $mylimit )
    echo "Removing" $lines[$mycount]
        sudo apt-get -y remove $lines[$mycount]
    echo "...done"
    @ mycount = $mycount + 1
end
