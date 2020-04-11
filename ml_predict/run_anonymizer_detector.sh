#Actiavte the environemtn where the dependencies are contained
conda activate virus
#Run anonymizer on the input image
PYTHONPATH=$PYTHONPATH:. python ./anonymizer/bin/anonymize.py --input ./1-input-images  --image-output ./2-anonymized-images --weights ./weights
#Run people detector on the input image
#python nanonetes_predict.py	

