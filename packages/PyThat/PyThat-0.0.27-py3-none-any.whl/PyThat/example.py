# from PyThat import MeasurementTree
from h5to_nc import MeasurementTree
import xarray as xr
import matplotlib.pyplot as plt

# Define path to .h5 file
paths = [r'D:\Pycharm\PyThat\examples\floquet_just_spectrum_analyzer_large_incomplete.h5',
        r"D:\Pycharm\PyThat\examples\Spot_characterization_Thorlabs_R1DS2N_slit_hi_res.h5",
        r'D:\Pycharm\PyThat\examples\Spot_characterization_on_Thorlabs_R1DS2N_across_slit_hi_res.h5',
        r"D:\Pycharm\PyThat\examples\100mm_scan_radius - Kopie.h5"]
# index = (2, 1)
# index = (3,0)
# Optional: If the index is known beforehand, it can be specified here. Otherwise the user will be asked to choose.
# index = (2, 1)

# Create measurement_tree object. Path argument should point towards thatec h5 file.
out = []
for path in paths:
    measurement_tree = MeasurementTree(path, index=True, override=False)
    out.append(measurement_tree)
    print()
    print(f'self.logs: {measurement_tree.logs}')
    print(f'self.devices: {measurement_tree.devices}')
    print(f'self.labbook: {measurement_tree.labbook}')
    print(f'self.tree_string:\n{measurement_tree.tree_string}')

for i in out:
    # print(i.dataset)
    i.dataset[list(i.dataset.data_vars)[0]].plot()
    plt.show()


exit()
data: xr.DataArray = measurement_tree.array
data.isel({'Set Magnetic Field': 5}).plot()


plt.show()
