# install it into ...

if ( "$1" == "" ) then
echo "You need a ROOT version number in this format X.XX.XX"
exit 1
endif

set ROOT_VER = $1
echo "The root version is: $ROOT_VER"
set CURRENT_PATH=`pwd`
echo "Current directory is: ${CURRENT_PATH}"
set ROOT_TAG = "root-${ROOT_VER}"
echo "The root TAG is: $ROOT_TAG"

#change according to user (give full path):
set DOWNLOAD_DIR = "/home/ecarrera/Downloads"

echo "The directory where everything will downloaded is: ${DOWNLOAD_DIR}"
set ROOT_TARFILE = "root_v${ROOT_VER}.source.tar.gz"
set ROOT_TARFILE_PATH = "${DOWNLOAD_DIR}/${ROOT_TARFILE}"
echo "We will search for this tar file: $ROOT_TARFILE_PATH"
set ROOT_DOWNLOAD_LOCATION = "https://root.cern.ch/download"
echo "Root will be downloaded from ${ROOT_DOWNLOAD_LOCATION} if it does not exist yet"
set ROOT_SOURCE="${DOWNLOAD_DIR}/$ROOT_TAG"
echo "Root will be built from this source directory: $ROOT_SOURCE"

#change according to user (give full path):
set ROOT_USER_DIR="/home/ecarrera"

echo "The user directory to use is set to: ${ROOT_USER_DIR}"
set ROOT_BUILD="${ROOT_USER_DIR}/root_builds_dir/${ROOT_TAG}_buildir"
echo "Root will be build at: $ROOT_BUILD"
set ROOT_INSTALL_DIR="/usr/local/ROOT/$ROOT_TAG"
echo "Root will be installed at: ${ROOT_INSTALL_DIR}"

#check if root tar file exists, if not, download it from repository
if ( -f ${ROOT_TARFILE_PATH} ) then
echo "${ROOT_TARFILE_PATH} exists already. We will be using it ..."
else
echo "${ROOT_TARFILE_PATH} does not exist yet, we will try to download it ..."
wget ${ROOT_DOWNLOAD_LOCATION}/${ROOT_TARFILE} -P ${DOWNLOAD_DIR}
endif

#unpack the tar file if needed
if (-d ${ROOT_SOURCE}) then
echo "${ROOT_SOURCE} source directory exists, we will attempt to use its contents to build ROOT ..."
else
echo "Unpacking ${ROOT_TARFILE_PATH} in ${DOWNLOAD_DIR} ..."
cd ${DOWNLOAD_DIR}
tar xfvz ${ROOT_TARFILE_PATH}
cd ${CURRENT_PATH}
endif

#check if there is already a build directory with the same name, if not, create one
if ( -d ${ROOT_BUILD} ) then
echo "${ROOT_BUILD} exists already. Please check that you are not overwriting and try again..... quiting"
exit 1
else
echo "${ROOT_BUILD} directory will be created ..."
mkdir -p ${ROOT_BUILD}
endif

#check if there is already an install directory with the same name, if not, create one
if ( -d ${ROOT_INSTALL_DIR} ) then
echo "${ROOT_INSTALL_DIR} exists already. Please check that you are not overwriting and try again..... quiting"
exit 1
else
echo "${ROOT_INSTALL_DIR} directory will be created.  You might need superpowers ..."
sudo mkdir -p ${ROOT_INSTALL_DIR}
endif


#rm -rf ${ROOT_INSTALL_DIR}
#sudo mkdir -p ${ROOT_INSTALL_DIR}
# download, unpack and build it in /tmp
#cd /tmp
#rm -rf root-build root-6.06.06 root_v6.06.06.source.tar.gz*
#wget https://root.cern.ch/download/root_v6.06.06.source.tar.gz
#tar zxvf ~/Downloads/root_v6.08.02.source.tar.gz


#mkdir root-6.08.02_builddir
#cd root-6.08.02_builddir
#unset ROOTSYS
#cmake -DCMAKE_INSTALL_PREFIX="${ROOT_INSTALL_DIR}" -Dall="ON" -Dgeocad="ON" -Dbuiltin_ftgl="OFF" -Dbuiltin_glew="OFF" -Dsoversion="ON" $ROOT_SOURCE
#make
#sudo cmake --build . --target install
# final cleanup
#cd ../
#rm -rf root-build root-6.06.06 root_v6.06.06.source.tar.gz*
