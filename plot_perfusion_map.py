import os
import SimpleITK as sitk
import matplotlib
# matplotlib.use('Agg')
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def plot(src_dir,tgt_dir,subtract=False):
	print(src_dir, "subtract: {}".format(subtract))
	if not os.path.exists(src_dir):
		return

	reader = sitk.ImageFileReader()
	reader.SetFileName(os.path.join(src_dir,"mIP.nii.gz"))
	image = reader.Execute()

	reader.SetFileName(os.path.join(src_dir,"mIP_tumor.nii.gz"))
	label = reader.Execute()

	reader.SetFileName(os.path.join(src_dir,"mIP_temporal_mIP_1-3.nii.gz"))
	image_0 = reader.Execute()
	reader.SetFileName(os.path.join(src_dir,"mIP_temporal_mIP_4-7.nii.gz"))
	image_1 = reader.Execute()
	reader.SetFileName(os.path.join(src_dir,"mIP_temporal_mIP_8-10.nii.gz"))
	image_2 = reader.Execute()

	castFilter = sitk.CastImageFilter()
	castFilter.SetOutputPixelType(sitk.sitkFloat32)
	label = castFilter.Execute(label)

	maskFilter = sitk.MaskNegatedImageFilter()
	maskFilter.SetMaskingValue(1)
	image_0 = maskFilter.Execute(image_0,label)
	image_1 = maskFilter.Execute(image_1,label)
	image_2 = maskFilter.Execute(image_2,label)

	binaryThresholdFilter = sitk.BinaryThresholdImageFilter()
	binaryThresholdFilter.SetLowerThreshold(256)
	binaryThresholdFilter.SetUpperThreshold(1024)
	binaryThresholdFilter.SetInsideValue(1)

	mask_0 = binaryThresholdFilter.Execute(image_0)
	mask_1 = binaryThresholdFilter.Execute(image_1)
	mask_2 = binaryThresholdFilter.Execute(image_2)
	castFilter.SetOutputPixelType(sitk.sitkFloat32)
	mask_0 = castFilter.Execute(mask_0)
	mask_1 = castFilter.Execute(mask_1)
	mask_2 = castFilter.Execute(mask_2)

	image_0 = maskFilter.Execute(image_0,mask_0)
	image_1 = maskFilter.Execute(image_1,mask_1)
	image_2 = maskFilter.Execute(image_2,mask_2)

	intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(300);
	intensityWindowingFilter.SetWindowMinimum(0);
	image = intensityWindowingFilter.Execute(image)

	intensityWindowingFilter.SetOutputMaximum(255)
	intensityWindowingFilter.SetOutputMinimum(0)
	intensityWindowingFilter.SetWindowMaximum(512);
	intensityWindowingFilter.SetWindowMinimum(0);
	image_0 = intensityWindowingFilter.Execute(image_0)
	image_1 = intensityWindowingFilter.Execute(image_1)
	image_2 = intensityWindowingFilter.Execute(image_2)

	pbar = tqdm(range(image.GetSize()[2]))
	for i in pbar:
		# if not i == 8:
		# 	continue
		image_slice = sitk.GetArrayFromImage(image)[i,:,:]
		mask_slice = sitk.GetArrayFromImage(label)[i,:,:]
		image_slice_0 = sitk.GetArrayFromImage(image_0)[i,:,:]
		image_slice_1 = sitk.GetArrayFromImage(image_1)[i,:,:]
		image_slice_2 = sitk.GetArrayFromImage(image_2)[i,:,:]

		dpi = 100
		shape=np.shape(image_slice)[0:2][::-1]
		size = [float(i)/dpi for i in shape]
		size[0] = size[0]*4

		my_cmap = matplotlib.cm.jet
		my_cmap.set_under((1, 1, 1, 0))

		fig = plt.figure()
		fig.set_size_inches(size)
		ax = plt.Axes(fig,[0,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(image_slice,cmap="gray",origin='lower')

		ax = plt.Axes(fig,[0.25,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(image_slice,cmap="gray",origin='lower')
		if np.max(image_slice_0) > 1:
			ax0 = ax.imshow(image_slice_0,cmap=my_cmap,origin='lower',alpha=.9, vmin=1, vmax=255)

		ax = plt.Axes(fig,[0.5,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(image_slice,cmap="gray",origin='lower')
		if subtract:
			if np.max(image_slice_1-image_slice_0) > 1:
				ax1 = ax.imshow(image_slice_1-image_slice_0,cmap=my_cmap,origin='lower',alpha=.9, vmin=1, vmax=255)		
		else:
			if np.max(image_slice_1) > 1:
				ax1 = ax.imshow(image_slice_1,cmap=my_cmap,origin='lower',alpha=.9, vmin=1, vmax=255)

		ax = plt.Axes(fig,[0.75,0,0.25,1])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(image_slice,cmap="gray",origin='lower')
		if subtract:
			if np.max(image_slice_2-image_slice_1) > 1:
				ax2 = ax.imshow(image_slice_2-image_slice_1,cmap=my_cmap,origin='lower',alpha=.9, vmin=1, vmax=255)
		else:
			if np.max(image_slice_2) > 1:
				ax2 = ax.imshow(image_slice_2,cmap=my_cmap,origin='lower',alpha=.9, vmin=1, vmax=255)

		if np.sum(mask_slice) > 0:
			cax = fig.add_axes([0.27, 0.1, 0.5, 0.025])

			if "ax0" in locals():
				cb = fig.colorbar(ax0, ticks=[1, 63, 127, 191, 255],cax=cax, orientation='horizontal')
			elif "ax1" in locals():
				cb = fig.colorbar(ax1, ticks=[1, 63, 127, 191, 255],cax=cax, orientation='horizontal')
			elif "ax2" in locals():
				cb = fig.colorbar(ax2, ticks=[1, 63, 127, 191, 255],cax=cax, orientation='horizontal')
			
			if "cb" in locals():
				cb.set_label('HU value', color='white')
				cb.ax.xaxis.set_tick_params(color='white')
				cb.outline.set_edgecolor('white')
				plt.setp(plt.getp(cb.ax.axes, 'xticklabels'), color='white')

				xtickvalues = [str(i*512/4) for i in range(5)]
				cb.ax.set_xticklabels(xtickvalues)

		# plt.show()

		if not os.path.exists(tgt_dir):
			os.makedirs(tgt_dir)
		fig.savefig(os.path.join(tgt_dir,str(i+1) + ".jpg"),dpi=dpi)
		plt.close(fig)

def main():
	data_dir = "Z:/data/liver/by_case"

	stages = ["pre","post"]
	# cases = ["YauWaiBor"]

	for case in os.listdir(data_dir):
		# if not case in cases:
		# 	continue
		for stage in stages:
			if stage == "pre":
				src_dir = os.path.join(data_dir,case, stage, "nii_reg","HA")
				tgt_dir = os.path.join(data_dir,case,"plot","perfusion_pre")
			else:
				src_dir = os.path.join(data_dir,case, stage, "nii_reg_pre","HA")
				tgt_dir = os.path.join(data_dir,case,"plot","perfusion_post")

			plot(src_dir,tgt_dir,subtract=False)

			if stage == "pre":
				src_dir = os.path.join(data_dir,case, stage, "nii_reg","HA")
				tgt_dir = os.path.join(data_dir,case,"plot","perfusion_pre_subtract")
			else:
				src_dir = os.path.join(data_dir,case, stage, "nii_reg_pre","HA")
				tgt_dir = os.path.join(data_dir,case,"plot","perfusion_post_subtract")

			plot(src_dir,tgt_dir,subtract=True)
		# exit()

if __name__ == "__main__":
	main()