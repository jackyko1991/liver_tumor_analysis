import SimpleITK as sitk
import os
from tqdm import tqdm

def segmentation2D(image_path, mask_path, mip_path, label_path):
	reader = sitk.ImageFileReader()

	reader.SetFileName(image_path)
	image = reader.Execute()

	reader.SetFileName(mask_path)
	mask = reader.Execute()

	dilateFilter = sitk.BinaryDilateImageFilter()
	dilateFilter.SetKernelRadius(2)
	# mask = dilateFilter.Execute(mask)

	# mIP
	mipFilter = sitk.MaximumProjectionImageFilter()
	mipFilter.SetProjectionDimension(1)
	image = mipFilter.Execute(image)
	mask = mipFilter.Execute(mask)

	maskFilter = sitk.MaskImageFilter()
	tumor_image = maskFilter.Execute(image,mask)

	otsuFilter = sitk.OtsuMultipleThresholdsImageFilter()
	otsuFilter.SetNumberOfThresholds(4)
	label = otsuFilter.Execute(tumor_image)

	thresholdImageFilter = sitk.ThresholdImageFilter()
	thresholdImageFilter.SetLower(0)
	thresholdImageFilter.SetUpper(9999)
	image = thresholdImageFilter.Execute(image)

	thresholdFilter = sitk.BinaryThresholdImageFilter()
	thresholdFilter.SetUpperThreshold(4)
	thresholdFilter.SetLowerThreshold(3)
	thresholdFilter.SetOutsideValue(0)
	thresholdFilter.SetInsideValue(1)
	label = thresholdFilter.Execute(label)
	label = maskFilter.Execute(label,mask)

	writer = sitk.ImageFileWriter()
	writer.SetFileName(mip_path)
	writer.Execute(image)

	writer.SetFileName(label_path)
	writer.Execute(label)

def mIP3D(image_path, mip_path):
	if not os.path.exists(image_path):
		return

	reader = sitk.ImageFileReader()
	reader.SetFileName(image_path)
	image = reader.Execute()

	# mIP
	slice_num = 16

	for i in range(slice_num):
		roiFilter = sitk.RegionOfInterestImageFilter()
		roiFilter.SetSize((image.GetSize()[0],image.GetSize()[1],int(image.GetSize()[2]/slice_num)))
		roiFilter.SetIndex((0,0,i*int(image.GetSize()[2]/slice_num)))

		image_ = roiFilter.Execute(image)

		mipFilter = sitk.MaximumProjectionImageFilter()
		mipFilter.SetProjectionDimension(2)
		image__ = mipFilter.Execute(image_)

		if i == 0:
			image_mIP = image__
		else:
			tileFilter = sitk.TileImageFilter()
			layout = [1,1,2]
			tileFilter.SetLayout(layout)
			image_mIP = tileFilter.Execute(image_mIP,image__)

	image_mIP.SetOrigin((image.GetOrigin()[0],image.GetOrigin()[1],image.GetOrigin()[2]+image_mIP.GetSpacing()[2]/2))
	image_mIP.SetDirection(image.GetDirection())

	writer = sitk.ImageFileWriter()
	writer.SetFileName(mip_path)
	writer.Execute(image_mIP)

def mIP3D_old(image_path, mask_path, mip_path, label_path):
	if not (os.path.exists(image_path) and os.path.exists(mask_path)):
		return

	reader = sitk.ImageFileReader()

	reader.SetFileName(image_path)
	image = reader.Execute()

	reader.SetFileName(mask_path)
	mask = reader.Execute()

	dilateFilter = sitk.BinaryDilateImageFilter()
	dilateFilter.SetKernelRadius(2)
	# mask = dilateFilter.Execute(mask)

	# mIP
	slice_num = 16

	for i in range(slice_num):
		roiFilter = sitk.RegionOfInterestImageFilter()
		roiFilter.SetSize((image.GetSize()[0],image.GetSize()[1],int(image.GetSize()[2]/slice_num)))
		roiFilter.SetIndex((0,0,i*int(image.GetSize()[2]/slice_num)))

		image_ = roiFilter.Execute(image)
		mask_ = roiFilter.Execute(mask)

		mipFilter = sitk.MaximumProjectionImageFilter()
		mipFilter.SetProjectionDimension(2)
		image__ = mipFilter.Execute(image_)
		mask__ = mipFilter.Execute(mask_)

		if i == 0:
			image_mIP = image__
			mask_mIP = mask__
		else:
			tileFilter = sitk.TileImageFilter()
			layout = [1,1,2]
			tileFilter.SetLayout(layout)
			image_mIP = tileFilter.Execute(image_mIP,image__)
			mask_mIP = tileFilter.Execute(mask_mIP,mask__)

	image_mIP.SetOrigin((image.GetOrigin()[0],image.GetOrigin()[1],image.GetOrigin()[2]+image_mIP.GetSpacing()[2]/2))
	image_mIP.SetDirection(image.GetDirection())

	mask_mIP.SetOrigin((image.GetOrigin()[0],image.GetOrigin()[1],image.GetOrigin()[2]+image_mIP.GetSpacing()[2]/2))
	mask_mIP.SetDirection(image.GetDirection())

	writer = sitk.ImageFileWriter()
	writer.SetFileName(mip_path)
	writer.Execute(image_mIP)

	writer.SetFileName(label_path)
	writer.Execute(mask_mIP)

def main():
	data_dir = "Z:/data/liver/by_case"
	stages = ["pre","post"]

	pbar = tqdm(os.listdir(data_dir))

	for case in pbar:
	# for case in ["LeungHonMan"]:
		pbar.set_description(case)
		plain_path = os.path.join(data_dir,case,"pre","nii_reg","HA","plain.nii.gz")
		pre_HA_path = os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP.nii.gz")
		pre_PV_path = os.path.join(data_dir,case,"pre","nii_reg","PV","temporal_mIP.nii.gz")
		post_HA_path = os.path.join(data_dir,case,"post","nii_reg_pre","HA","temporal_mIP.nii.gz")
		post_PV_path = os.path.join(data_dir,case,"post","nii_reg_pre","PV","temporal_mIP.nii.gz")

		# 3d mip
		image_filenames = ["temporal_mIP_1-3.nii.gz","temporal_mIP_4-7.nii.gz","temporal_mIP_8-10.nii.gz"]
		# image_list = ["temporal_mIP","tumor_original_space.nii.gz","temporal_mIP_1-3","temporal_mIP_4-7","temporal_mIP_8-10"]

		for stage in stages:
			if stage == "pre":
				mip_path = os.path.join(data_dir,case,stage,"nii_reg","HA","mIP.nii.gz")
				label_path = os.path.join(data_dir,case,stage,"nii_reg","HA","mIP_tumor.nii.gz")
				mask_path = os.path.join(data_dir,case,stage,"nii_reg","HA","tumor_original_space.nii.gz")
				mIP3D(pre_HA_path, mip_path)
				mIP3D(mask_path,label_path)

				for image_filename in image_filenames:
					image_path = os.path.join(data_dir,case,stage,"nii_reg","HA",image_filename)
					mip_path = os.path.join(data_dir,case,stage,"nii_reg","HA","mIP_" + image_filename)						
					mIP3D(image_path, mip_path)
			elif stage == "post":
				mip_path = os.path.join(data_dir,case,stage,"nii_reg_pre","HA","mIP.nii.gz")
				label_path = os.path.join(data_dir,case,stage,"nii_reg_pre","HA","mIP_tumor.nii.gz")
				mask_path = os.path.join(data_dir,case,stage,"nii_reg_pre","HA","tumor_original_space.nii.gz")
				mIP3D(post_HA_path, mip_path)
				mIP3D(mask_path,label_path)

				for image_filename in image_filenames:
					image_path = os.path.join(data_dir,case,stage,"nii_reg_pre","HA",image_filename)
					mip_path = os.path.join(data_dir,case,stage,"nii_reg_pre","HA","mIP_" + image_filename)						
					mIP3D(image_path, mip_path)
if __name__ == "__main__":
	main()