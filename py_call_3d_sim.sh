#!/bin/bash
#User customizable files
layout_py="./example.py"
gds_result=$1
stl_binary_dir="./presentation_demo"
stl_ascii_dir="./presentation_demo_dir"
zip_to_file=$PWD
BW="5.0e8"
center_freq="60e9"
threads=2

#constant files
layout_stl_dir="./gdsiistl"
zipped_for_sim=sim_objects.zip
open_ems_dir="./rfems"
venv_activate_ems="./venv_3d/bin/activate"
venv_activate_stl="./venv_stl/bin/activate"
port_imp="50"
pitch=0.0001

#Ensure directories exist
./cleanup.sh
mkdir -p $stl_ascii_dir
mkdir -p $stl_binary_dir

echo "Copying gds file"
cp  $gds_result $stl_binary_dir
echo "Copying Finished"


#Convert layout to stl
echo "Converting layout to stl."
source $venv_activate_stl
pushd $PWD
pushd $layout_stl_dir
python3 "gdsiistl.py" "../$stl_binary_dir/$gds_result"
popd
echo "Conversion complete."

#Convert all binary stl files to ascii stl
echo "Converting stl to ascii."
./convert2ascii.sh "$stl_binary_dir"

#Move ascii files to new directory and label them correctly
for asciifile in "$stl_binary_dir"/*.ascii; do
	filename=$(basename "$asciifile")
	base_name="${filename%.*}"
	mv "$asciifile" "$stl_ascii_dir/$base_name"
done
echo "Ascii conversion complete."

#Zip up files
echo "Zipping files."
zip -r $zipped_for_sim $stl_ascii_dir/*
echo "Zipping complete."

#Run openEMS
source $venv_activate_ems
pushd $open_ems_dir

echo "Beggining Simulation."
python3 rfems.py "../$zipped_for_sim" --freq $center_freq --span $BW --line $port_imp --thread $threads --pitch $pitch
echo "Simulation complete."

