import SimpleITK as sitk
import os
import shutil
from tqdm import tqdm

def main():
	data_dir = "Z:/data/liver/by_case"
	executable = "D:/projects/liver_tumor/binary/ExpertAutomatedRegistration.exe"
	resample_exe = "D:/projects/liver_tumor/binary/ResampleScalarVectorDWIVolume.exe"

	selected = ["ChungWahKitFacchetti"]
	ignore = ["WongPunCheong"]
	phases = ["HA","PV"]
	images = ["temporal_mIP.nii.gz","temporal_mIP_1-3.nii.gz","temporal_mIP_4-7.nii.gz","temporal_mIP_8-10.nii.gz","01.nii.gz","02.nii.gz","03.nii.gz","04.nii.gz","05.nii.gz","06.nii.gz","07.nii.gz","08.nii.gz","09.nii.gz","10.nii.gz"]

	pbar = tqdm(selected)
	# pbar = tqdm(os.listdir(data_dir))

	for patient in pbar:
		if patient in ignore:
			continue

		if not os.path.exists(os.path.join(data_dir,patient,"LinearTransform.tfm")):
			continue

		if os.path.isdir(os.path.join(data_dir, patient)):
			pbar.set_description(patient)
			
			for phase in phases:
				# clear target directory
				# shutil.rmtree(os.path.join(data_dir,patient,"post","nii_reg_pre",phase),ignore_errors=True)
				os.makedirs(os.path.join(data_dir,patient,"post","nii_reg_pre",phase),exist_ok=True)

				# registration 
				for image in images:
					fixed = os.path.join(data_dir,patient,"pre","nii_reg","HA","temporal_mIP.nii.gz")
					moving = os.path.join(data_dir,patient,"post","nii_reg",phase,image)
					resample = os.path.join(data_dir,patient,"post","nii_reg_pre",phase,image)
					initialization = os.path.join(data_dir,patient,"LinearTransform.tfm")
					tfm = os.path.join(data_dir,patient,"BSplineTransform.tfm")

					if not os.path.exists(moving):
						continue

					if image == "temporal_mIP.nii.gz":
						command = executable + " " + \
							"--registration BSpline " + \
							"--initialization None " + \
							"--loadTransform " + initialization + " " +\
							"--saveTransform " + tfm + " "+\
							"--resampledImage " + resample + " "+\
							fixed + " " +\
							moving
					else:
						command = executable + " " + \
							"--registration BSpline " + \
							"--initialization None " + \
							"--loadTransform " + initialization + " " +\
							"--resampledImage " + resample + " "+\
							fixed + " " +\
							moving
					os.system(command)

					# exit()

if __name__ == "__main__":
	main()