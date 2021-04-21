*This is a test repository. Once I am certain that I am going into the right direction, I will move everything to a fresh repository `snapshot-gnss-data` that will eventually go public.*

# GNSS Snapshot Utilities

Author: *Jonas Beuchert*

This repository contains open-source Python utilities to read the raw GNSS snapshots from the dataset

> *Data citation, including DOI.*

The class `dataset.Dataset` can represent a single dataset that was recorded with a SnapperGPS receiver and offers methods to access the data.

## Dependencies

The code was tested with Python 3.7.10 on Ubuntu 18 and macOS Big Sur and with Python 3.7.7 on Windows 10.

The basic functionality requires `numpy`. In addition, working with ground truth data requires `pymap3d` and `Shapely`. You can install all three packages via `pip` with the `requirements.txt` file in this repository

```shell
python -m pip install -r requirements.txt
```

## Usage

If you want to read the GNSS signal snapshot with index 19 from the dataset stored in the directory `data/J`, then type

```python repl
>>> import dataset
>>> ds = dataset.Dataset("data/J")
Open ground truth file of type gpx.
>>> ds.get_snapshot(19)
array([ 1,  1,  1, ..., -1, -1, -1], dtype=int8)
```

To view an estimate of the intermediate frequency at which the GNSS signal was recorded, type

```python repl
>>> ds.get_intermediate_frequency()
4091232.0
```

To obtain the timestamps that are associated with the recorded snapshots, type

```python repl
>>> ds.get_timestamps()
array(['2021-03-24T10:37:46.000', ..., '2021-03-24T11:42:19.000'],
      dtype='datetime64[ms]')
```

If you calculated a position from the raw snapshot and want to compare it to the ground truth, type

```python repl
>>> ds.get_error(my_estimated_latitude, my_estimated_longitude)
2.3513792721992006
```

To view the full class documentation, type

```python repl
>>> import dataset
>>> help(dataset.Dataset)
Help on class Dataset in module dataset:

class Dataset(builtins.object)
 |  Dataset(directory)
 |  
 |  GNSS snapshot dataset representation.
 |  
 |  Methods
 |  -------
 |  get_size()
 |      Get number of snapshots in dataset, i.e., size of dataset.
 |  get_snapshot(idx, normalize=False)
 |      Get specific raw GNSS signal snapshot.
 |  get_ground_truth()
 |      Get ground truth location or track.
 |  get_intermediate_frequency()
 |      Get intermediate frequency.
 |  get_timestamps()
 |      Get all times when measurements were taken / snapshots were captured.
 |  get_temperatures()
 |      Get all temperature measurements.
 |  get_pressures()
 |      Get all pressure measurements.
 |  get_error(self, latitude, longitude)
 |      Calculate horizontal error w.r.t. ground truth point / track.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, directory)
 |      Create snapshot dataset representation.
 |      
 |      Parameters
 |      ----------
 |      directory : string
 |          Dataset directory that contains the binary raw data as .bin files,
 |          other data as meta.json file, and potentially ground truth tracks
 |          as .kml or .gpx file(s).
 |      
 |      Returns
 |      -------
 |      None.
 |  
 |  get_error(self, latitude, longitude)
 |      Calculate horizontal error w.r.t. ground truth point / track.
 |      
 |      Parameters
 |      ----------
 |      latitude : float
 |          Latitude of test location [°].
 |      longitude : float
 |          Longitude of test location [°].
 |      
 |      Returns
 |      -------
 |      float
 |          Horizontal (2D) Euclidean distance [m] between test location and
 |          ground truth location / or next location on ground truth track.
 |  
 |  get_ground_truth(self)
 |      Get ground truth location or track.
 |      
 |      Returns
 |      -------
 |      dict {"latitude": float, "longitude": float}
 |      or list of dict {"latitude": float, "longitude": float}
 |          Dictionary with static ground truth location or list of
 |          dictionaries for ground truth track. The list defines a polyline,
 |          which nodes are not directly related to snapshots.
 |  
 |  get_intermediate_frequency(self)
 |      Get intermediate frequency.
 |      
 |      Returns
 |      -------
 |      float
 |          Intermediate frequency [Hz].
 |  
 |  get_pressures(self)
 |      Get all pressure measurements.
 |      
 |      Returns
 |      -------
 |      numpy.ndarray, dtype=float64, shape=(N,)
 |          List of ambient pressures [Pa].
 |  
 |  get_size(self)
 |      Get number of snapshots in dataset, i.e., size of dataset.
 |      
 |      Returns
 |      -------
 |      int
 |          Number of snapshots in dataset.
 |  
 |  get_snapshot(self, idx, normalize=False)
 |      Get specific raw GNSS signal snapshot.
 |      
 |      Parameters
 |      ----------
 |      idx : int
 |          Index of file / snapshot.
 |      normalize : bool, optional
 |          Subtract mean from signal. The default is False.
 |      
 |      Returns
 |      -------
 |      np.ndarray, dtype=int8 if normalize=False, dtype=float32 if
 |      normalize=True, shape=(49104,)
 |          Binary raw GNSS snapshot with length 12 ms sampled at 4.092 MHz.
 |          Samples element of {-1, +1} if normalize=False.
 |          DC component removed, i.e., mean subtracted if normalize=True.
 |  
 |  get_temperatures(self)
 |      Get all temperature measurements.
 |      
 |      Returns
 |      -------
 |      numpy.ndarray, dtype=float64, shape=(N,)
 |          List of ambient temperatures [°C].
 |  
 |  get_timestamps(self)
 |      Get all times when measurements were taken / snapshots were captured.
 |      
 |      Returns
 |      -------
 |      numpy.ndarray, dtype=numpy.datetime64[ms], shape=(N,1)
 |          Timestamps in UTC.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```
