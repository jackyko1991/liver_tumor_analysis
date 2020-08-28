import os
import SimpleITK as sitk
from tqdm import tqdm
import numpy as np

def main():
	src_dir = "Z:/data/liver/by_case"
	tgt_filename = "temporal_mIP.nii.gz"

	# cases = ["ChungWahKitFacchetti","LamMoChe","SitLeongWor","TamSunnyKing","WongNaiKeung","WongWaiLun","WongYiu","YauPoHing"]
	cases = ["YauPoHing"]
	# cases = os.listdir(src_dir)[16:]

	pbar = tqdm(cases)
	stages = ["pre","post"]
	phases = ["HA","PV"]

	for case in pbar:
		pbar.set_description(case)
		for stage in stages:
			for phase in phases:
				if not os.path.exists(os.path.join(src_dir,case,stage,"nii_reg",phase)):
					continue

				images = []
				images_np = []
				for time in range(1,11):
					if time < 10:
						filename = os.path.join(src_dir,case,stage,"nii_reg",phase,"0"+str(time)+".nii.gz")
					else:
						filename = os.path.join(src_dir,case,stage,"nii_reg",phase,str(time)+".nii.gz")

					if not os.path.exists(filename):
						continue

					reader = sitk.ImageFileReader()
					reader.SetFileName(filename)
					image = reader.Execute()
					images.append(image)
					images_np.append(sitk.GetArrayFromImage(image))

				images_np = np.stack(images_np,axis=-1)
				image_mIP_np = np.amax(images_np,axis=-1)
				
				# convert back to sitk image
				image_mIP = sitk.GetImageFromArray(image_mIP_np)
				image_mIP.SetDirection(images[0].GetDirection())
				image_mIP.SetSpacing(images[0].GetSpacing())
				image_mIP.SetOrigin(images[0].GetOrigin())

				writer = sitk.ImageFileWriter()
				writer.SetFileName(os.path.join(src_dir,case,stage,"nii_reg",phase,tgt_filename))
				writer.Execute(image_mIP)

				# 1-3s
				image_mIP_np = np.amax(images_np[:,:,:,0:3],axis=-1)
				
				# convert back to sitk image
				image_mIP = sitk.GetImageFromArray(image_mIP_np)
				image_mIP.SetDirection(images[0].GetDirection())
				image_mIP.SetSpacing(images[0].GetSpacing())
				image_mIP.SetOrigin(images[0].GetOrigin())

				writer = sitk.ImageFileWriter()
				writer.SetFileName(os.path.join(src_dir,case,stage,"nii_reg",phase,"temporal_mIP_1-3.nii.gz"))
				writer.Execute(image_mIP)

				# 4-7s
				image_mIP_np = np.amax(images_np[:,:,:,3:7],axis=-1)
				
				# convert back to sitk image
				image_mIP = sitk.GetImageFromArray(image_mIP_np)
				image_mIP.SetDirection(images[0].GetDirection())
				image_mIP.SetSpacing(images[0].GetSpacing())
				image_mIP.SetOrigin(images[0].GetOrigin())

				writer = sitk.ImageFileWriter()
				writer.SetFileName(os.path.join(src_dir,case,stage,"nii_reg",phase,"temporal_mIP_4-7.nii.gz"))
				writer.Execute(image_mIP)

				# 1-3s
				image_mIP_np = np.amax(images_np[:,:,:,7:],axis=-1)
				
				# convert back to sitk image
				image_mIP = sitk.GetImageFromArray(image_mIP_np)
				image_mIP.SetDirection(images[0].GetDirection())
				image_mIP.SetSpacing(images[0].GetSpacing())
				image_mIP.SetOrigin(images[0].GetOrigin())

				writer = sitk.ImageFileWriter()
				writer.SetFileName(os.path.join(src_dir,case,stage,"nii_reg",phase,"temporal_mIP_8-10.nii.gz"))
				writer.Execute(image_mIP)



if __name__=="__main__":
	main()