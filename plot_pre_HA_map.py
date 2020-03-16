import os
import SimpleITK as sitk
import matplotlib
# matplotlib.use('Agg')
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def main():
	data_dir = "./data/by_case"

	for case in os.listdir(data_dir):
		reader = sitk.ImageFileReader()
		reader.SetFileName(os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP.nii.gz"))
		image = reader.Execute()

		reader.SetFileName(os.path.join(data_dir,case,"pre","nii_reg","HA","label.nii.gz"))
		label = reader.Execute()

		reader.SetFileName(os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP_1-3.nii.gz"))
		image_0 = reader.Execute()
		reader.SetFileName(os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP_4-7.nii.gz"))
		image_1 = reader.Execute()
		reader.SetFileName(os.path.join(data_dir,case,"pre","nii_reg","HA","temporal_mIP_8-10.nii.gz"))
		image_2 = reader.Execute()

		castFilter = sitk.CastImageFilter()
		castFilter.SetOutputPixelType(sitk.sitkFloat32)
		label = castFilter.Execute(label)

		maskFilter = sitk.MaskNegatedImageFilter()
		maskFilter.SetMaskingValue(2)
		image_0 = maskFilter.Execute(image_0,label)
		image_1 = maskFilter.Execute(image_1,label)
		image_2 = maskFilter.Execute(image_2,label)

		intensityWindowingFilter = sitk.IntensityWindowingImageFilter()
		intensityWindowingFilter.SetOutputMaximum(255)
		intensityWindowingFilter.SetOutputMinimum(0)
		intensityWindowingFilter.SetWindowMaximum(300);
		intensityWindowingFilter.SetWindowMinimum(0);
		image = intensityWindowingFilter.Execute(image)
		image_0 = intensityWindowingFilter.Execute(image_0)
		image_1 = intensityWindowingFilter.Execute(image_1)
		image_2 = intensityWindowingFilter.Execute(image_2)

		for i in range(image.GetSize()[0]):
			if not i == 22:
				continue
			image_slice = sitk.GetArrayFromImage(image)[i,:,:]
			image_slice_0 = sitk.GetArrayFromImage(image_0)[i,:,:]
			image_slice_1 = sitk.GetArrayFromImage(image_1)[i,:,:]
			image_slice_2 = sitk.GetArrayFromImage(image_2)[i,:,:]

			fig = plt.figure()
			a = fig.add_subplot(2, 2, 1)
			imgplot = plt.imshow(image_slice,cmap="gray")
			plt.axis('off')
			a.set_title('Temporal mIP 1-10s')
			a.invert_yaxis()

			my_cmap = matplotlib.cm.jet
			my_cmap.set_under((1, 1, 1, 0))

			a = fig.add_subplot(2, 2, 2)
			imgplot = plt.imshow(image_slice,cmap="gray")
			imgplot = plt.imshow(image_slice_0,cmap=my_cmap,alpha=.9, vmin=1)
			plt.axis('off')
			a.set_title('Temporal mIP 1-3s')
			a.invert_yaxis()

			a = fig.add_subplot(2, 2, 3)
			imgplot = plt.imshow(image_slice,cmap="gray")
			imgplot = plt.imshow(image_slice_1,cmap=my_cmap,alpha=.9, vmin=1)
			plt.axis('off')
			a.set_title('Temporal mIP 4-7s')
			a.invert_yaxis()

			a = fig.add_subplot(2, 2, 4)
			imgplot = plt.imshow(image_slice,cmap="gray")
			imgplot = plt.imshow(image_slice_2,cmap=my_cmap,alpha=.9, vmin=1)
			plt.axis('off')
			a.set_title('Temporal mIP 8-10s')
			a.invert_yaxis()

			plt.show()


		exit()

if __name__ == "__main__":
	main()