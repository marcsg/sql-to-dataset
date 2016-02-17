#!/bin/bash

output="output"
backupDir="backup";

if [ ! -d $output ]; then
  mkdir $output;
  echo "Output folder $output created.";
else
  rm -rf $output/*.xml;
  echo "Output folder $output exists. XML files removed.";
fi

if [ ! -d $backupDir ]; then
  mkdir $backupDir;
fi;

./sql-to-dataset.py -i ~/pi.xml -t PRICEABLE_ITEM -o $output/1pi.xml;
./sql-to-dataset.py -i ~/sp.xml -t STORED_PRICE -o $output/2sp.xml;
./sql-to-dataset.py -i ~/dest.xml -t PRICEABLE_DESTINATION_CHANNEL -o $output/3dest.xml;
./sql-to-dataset.py -i ~/pe.xml -t PRICE_EVENT -o $output/4pe.xml;
./sql-to-dataset.py -i ~/pep.xml -t PRICE_EVENT_PRICEABLE -o $output/5pep.xml;
./sql-to-dataset.py -i ~/psi.xml -t PRICE_SCHEDULE_ITEM -o $output/6psi.xml;
./sql-to-dataset.py -i ~/pepe.xml -t PRICE_EVENT_PRICEABLE_ERROR -o $output/7pepe.xml;
./sql-to-dataset.py -i ~/po.xml -t PRICE_OVERRIDE -o $output/8po.xml;

echo ""

datasetFile="dataset.xml";
if [ -f $datasetFile ]; then
  timestamp=`date +"%Y-%m-%d-%H%M%S"`;
  echo "Backup existing $datasetFile to $backupDir/$datasetFile.$timestamp";
  mv $datasetFile $backupDir/$datasetFile.$timestamp;
fi;

for i in `ls -t $output/*.xml`;
do
  cat $i | grep -v dataset | sed '/^\s*$/d' >> $datasetFile;
done;

echo "Dataset file $datasetFile saved.";
