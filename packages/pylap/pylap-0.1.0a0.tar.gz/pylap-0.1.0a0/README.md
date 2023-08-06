## Install Instructions
1. Download and install PHaRLAP toolbox for matlab as directed
2. Download Pylap 
3. Ensure you have an Intel Compiler. The one used originally is availible at the following download link: https://registrationcenter-download.intel.com/akdlm/irc_nas/17113/l_comp_lib_2020.4.304_comp.for_redist.tgz
4. cd into the intel compiler folder and run install.sh, follow the prompt until install complete
```
4. export PHARLAP_HOME="your path to pharlap install dir"
5. export LD_LIBRARY="/<YOUR PATH TO DIR>/l_comp_lib_2020.4.304_comp.for_redist/compilers_and_libraries_2020.4.304/linux/compiler/lib/intel64_lin" 
6. export DIR_MODELS_REF_DAT="${PHARLAP_HOME}/dat"
7. sudo apt-get install python3-tk python3-pil python3-pil.imagetk libqt5gui5 python3-pyqt5 
8. sudo apt-get install libxcb-randr0-dev libxcb-xtest0-dev libxcb-xinerama0-dev libxcb-shape0-dev libxcb-xkb-dev
9. source /home/${username}/bin/compilervars.sh intel64
10. sudo python3 setup.py install
```
12. Use Example folder files as templates to test the installation


