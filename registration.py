import os
import shutil
from tqdm import tqdm

def main():
	executable = "D:/projects/liver_tumor/binary/ExpertAutomatedRegistration.exe"
	working_dir = "Z:/data/liver/by_case"

	# cases = os.listdir(working_dir)
	cases = ["ChungWahKitFacchetti","LamMoChe","SitLeongWor","TamSunnyKing","WongNaiKeung","WongWaiLun","WongYiu","YauPoHing"]
	ignore = ["ChoySimWang","HuiSiuKuenMary","KowkMenYee","LeungKwokMan","WongMukChing","ChuKitPing"]

	pbar = tqdm(cases)
	for patient in pbar:
		if patient in ignore:
			continue

		if os.path.isdir(os.path.join(working_dir, patient)):
			pbar.set_description(patient)

			for stage in os.listdir(os.path.join(working_dir, patient)):
				for phase in os.listdir(os.path.join(working_dir, patient,stage, "nii_crop")):
					tqdm.write("{} {}".format(stage, phase))

					# clear target directory
					shutil.rmtree(os.path.join(working_dir,patient,stage,"nii_reg",phase),ignore_errors=True)
					os.makedirs(os.path.join(working_dir,patient,stage,"nii_reg",phase),exist_ok=True)

					# register to plain data
					for file in os.listdir(os.path.join(working_dir, patient,stage, "nii_crop",phase)):
						if file == "plain.nii.gz":
							src = os.path.join(working_dir,patient,stage,"nii_crop",phase,"plain.nii.gz")
							tgt = os.path.join(working_dir,patient,stage,"nii_reg",phase,"plain.nii.gz")
							shutil.copy(src,tgt)
						else:
							fixed = os.path.join(working_dir,patient,stage,"nii_crop",phase,"plain.nii.gz")
							moving = os.path.join(working_dir, patient, stage, "nii_crop", phase, file)
							resample = os.path.join(working_dir,patient,stage,"nii_reg",phase,file[-9:-7] + ".nii.gz")
							tfm = os.path.join(working_dir,patient,stage, "nii_reg", phase, "transform_"+ file[-9:-7] + ".tfm")

							command = executable + " " + \
								"--registration BSpline " + \
								"--initialization None " + \
								"--saveTransform " + tfm + " "+\
								"--resampledImage " + resample + " "+\
								fixed + " " +\
								moving
							os.system(command)
							# exit()

						# # apply registration transform to  data
						# command = executable + " " + \
						# 	"--registration Initial " + \
						# 	"--initialization None " + \
						# 	"--loadTransform " + tfm + " " +\
						# 	"--resampledImage " + resample + " "+\
						# 	fixed + " " +\
						# 	moving

					# if stage != "HA"

					# if stage == "post":
					# 	continue
					# if phase == "plain":
					# 	source_file = os.path.join(os.path.join(working_dir,patient,stage,"nii_crop","plain.nii.gz"))
					# 	target_file = os.path.join(working_dir,patient,stage,"nii_reg","plain.nii.gz")
					# 	shutil.copyfile(source_file, target_file)
					# 	continue
					# else:
					# 	# clear target directory
					# 	shutil.rmtree(os.path.join(working_dir,patient,stage,"nii_reg",phase),ignore_errors=True)
					# 	os.makedirs(os.path.join(working_dir,patient,stage,"nii_reg",phase),exist_ok=True)

					# 	# # only register first data
					# 	# for file in os.listdir(os.path.join(working_dir, patient,stage, "nii",phase)):
					# 	# 	fixed = os.path.join(working_dir,patient,stage,"nii_crop","plain.nii.gz")
					# 	# 	moving = os.path.join(working_dir, patient, stage, "nii", phase, file)
					# 	# 	resample = os.path.join(working_dir,patient,stage,"nii_reg",phase,file[-9:-7] + ".nii.gz")
					# 	# 	tfm = os.path.join(working_dir,patient,stage, "nii_reg", phase, "transform.tfm")

					# 	# 	# command = executable + " " + \
					# 	# 	# 	"--registration Affine " + \
					# 	# 	# 	"--initialization None " + \
					# 	# 	# 	"--resampledImage " + resample + " "+\
					# 	# 	# 	fixed + " " +\
					# 	# 	# 	moving

					# 	# 	command = executable + " " + \
					# 	# 		"--registration BSpline " + \
					# 	# 		"--initialization None " + \
					# 	# 		"--saveTransform " + tfm + " "+\
					# 	# 		fixed + " " +\
					# 	# 		moving

					# 	# 	os.system(command)
					# 	# 	break

					# 	# apply registration transform to all data
					# 	for file in os.listdir(os.path.join(working_dir, patient,stage, "nii",phase)):
					# 		fixed = os.path.join(working_dir,patient,stage,"nii_crop","plain.nii.gz")
					# 		moving = os.path.join(working_dir, patient, stage, "nii", phase, file)
					# 		resample = os.path.join(working_dir,patient,stage,"nii_reg",phase,file[-9:-7] + ".nii.gz")
					# 		tfm = os.path.join(working_dir,patient,stage, "nii_reg", phase, "transform.tfm")

					# 		# command = executable + " " + \
					# 		# 	"--registration Initial " + \
					# 		# 	"--initialization None " + \
					# 		# 	"--loadTransform " + tfm + " " +\
					# 		# 	"--resampledImage " + resample + " "+\
					# 		# 	fixed + " " +\
					# 		# 	moving

					# 		command = executable + " " + \
					# 			"--registration PipelineAffine " + \
					# 			"--initialization None " + \
					# 			"--resampledImage " + resample + " "+\
					# 			fixed + " " +\
					# 			moving

					# 		os.system(command)
			
		# exit()

if __name__=="__main__":
	main()