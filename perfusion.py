import os
import numpy as np
import SimpleITK as sitk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm

def main():
	src_dir = "./data/by_case"

	pbar = tqdm(os.listdir(src_dir))

	stages = ["pre","post"]
	phases = ["HA","PV"]

	for case in pbar:
		pbar.set_description(case)
		for stage in stages:
			for phase in phases:
				images = []
				images_np = []

				reader = sitk.ImageFileReader()
				reader.SetFileName(os.path.join(src_dir,case,stage,"nii_reg",phase,"label.nii.gz"))
				label = reader.Execute()

				liver_value = []
				tumor_value = []

				for time in range(1,11):
					if time < 10:
						filename = os.path.join(src_dir,case,stage,"nii_reg",phase,"0"+str(time)+".nii.gz")
					else:
						filename = os.path.join(src_dir,case,stage,"nii_reg",phase,str(time)+".nii.gz")

					if not os.path.exists(filename):
						continue

					reader.SetFileName(filename)
					image = reader.Execute()
					images.append(image)

					statFilter = sitk.LabelStatisticsImageFilter()
					statFilter.Execute(image,label)
					liver_value.append(statFilter.GetMean(1))
					tumor_value.append(statFilter.GetMean(2))

				x = np.arange(len(images))
				plt.plot(x, liver_value,"o--", label=phase+"_liver")
				plt.plot(x, tumor_value,"o--", label=phase+"_tumor")
				plt.xlim(-0.5,9.5)
				plt.ylim(0,500)
				plt.legend()
				plt.xlabel("time")
				plt.ylabel("HU value")
			if stage == "pre":
				plt.title("Pre-Treatment")
			else:
				plt.title("Post-Treatment")
			plt.show()			
			plt.savefig(os.path.join(src_dir,case,stage,"perfusion_curve.jpg"))
			plt.clf()

		exit()

if __name__ == "__main__":
	main()