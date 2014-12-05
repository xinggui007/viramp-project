#!/bin/bash
#This script installs galaxy, clones viramp and run viramp on galaxy
#usage: sh runPipeline.sh <path>
#input: path- full path where you want it to be installed
#eg: sh runPipeline.sh /Users/aswathy/work/tmp


check_install() {
#checks to see if a command  is installed
  
   if command -v $1 >/dev/null 2>&1; then
          echo "$1 is installed"
   else
     echo "$1 is not installed; Installing ....."
     #exit 1
     easy_install $1
   fi
}


getGalaxy() {
#install galaxy in $INSTALL_DIR
   
   DIR=$1
   cd $DIR
   hg clone https://bitbucket.org/galaxy/galaxy-dist/   
}


getViramp() {
#install viramp in $INSTALL_DIR
   
   DIR=$1
   cd $DIR
   git clone https://github.com/ialbert/viramp-project.git    
}


run_galaxy() {
#create tool_config.xml with correct path

   DIR=$1
   gal_config_file="$DIR/galaxy-dist/config/tool_conf.xml"
   vamp_path="$DIR/viramp-project/script/vamp/"
   config_file="$DIR/viramp-project/config/tool_conf.xml" 
   pattern="vamp\/"
   sed -e "s|$pattern|$vamp_path|g" <$config_file >$gal_config_file
   
#run galaxy
   sh ${DIR}/galaxy-dist/run.sh
}

run() {
#runs the pipeline
    INSTALL_DIR=$1
    echo "checking to see if the install_dir exits ...."
    
    if [ ! -d "$INSTALL_DIR" ]; then
       echo "$INSTALL_DIR does not exist; creating $INSTALL_DIR ...."
       mkdir -p $INSTALL_DIR
    else
       echo "All good!! continuing ...."
    fi
    galaxy_run=${INSTALL_DIR}/galaxy-dist/run.sh

    echo "checking if galaxy is intsalled in $INSTALL_DIR ...."

    if [ -f "$galaxy_run" ]; then
       echo "galaxy is installed in ${INSTALL_DIR}"
    else
       echo "installing galaxy ..."
       getGalaxy ${INSTALL_DIR} 
    fi

    echo "checking if viramp is installed in $INSTALL_DIR ....."

    if [ -d "${INSTALL_DIR}/viramp-project" ]; then
         echo "viramp is installed in $INSTALL_DIR" 
    else
       echo "installing viramp in $INSTALL_DIR ...."
       getViramp ${INSTALL_DIR}
    fi

    echo "running viramp on galaxy ..."
    run_galaxy ${INSTALL_DIR}
    
}


#starting the script

#check_install hg

#INSTALL_DIR=$HOME/work/tmp/src

INSTALL_DIR=$1
run $INSTALL_DIR
