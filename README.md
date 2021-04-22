*This is a test repository. Once I am certain that I am going into the right direction, I will move everything to a fresh repository `snapshot-gnss-data` that will eventually go public.*

# GNSS Snapshot Dataset Utilities

Author: *Jonas Beuchert*

This repository contains open-source Python utilities to read the raw GNSS snapshots from the dataset

> *Data citation, including DOI.*

The class `dataset.Dataset` can represent a single dataset that was recorded with a SnapperGPS receiver and offers methods to access the data.

**Table of Contents**
1. [Dependencies](#dependencies)
2. [Usage](#usage)
3. [Data](#data)

## Dependencies

The code was tested with Python 3.7.10 on Ubuntu 18 and macOS Big Sur and with Python 3.7.7 on Windows 10.

The basic functionality requires `numpy`. In addition, working with ground truth data requires `pymap3d` and `Shapely`. You can install all three packages via `pip` with the `requirements.txt` file in this repository

```shell
python -m pip install -r requirements.txt
```

## Usage

If you want to read the GNSS signal snapshot with index `19` from the dataset stored in the directory `data/J`, then type

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
Still questions? [Go to Discussions](https://github.com/JonasBchrt/snapshot-gnss-data-test/discussions) or [open an Issue](https://github.com/JonasBchrt/snapshot-gnss-data-test/issues).

## Data

We published a detailed description of the data collection together with the collection itself, but here is a summary:

We recorded the data in 2020 and 2021 using three of our SnapperGPS low-cost receivers, which core components are an [Echo 27](https://www.siretta.com/products/antennas/echo-27/) GPS L1 antenna and a [SE4150L](https://www.skyworksinc.com/Products/Amplifiers/SE4150L) integrated GPS receiver circuit. Like most civilian low-cost GPS receivers, SnapperGPS operates in the L1 band with a centre frequency of 1.57542 GHz. However, Galileo's E1 signal, BeiDou's B1C signal, GPS' novel L1C signal, and SBAS' L1 signal have the identical centre frequency. So, we captured those signals, too. A SnapperGPS receiver down-mixes the incoming signal to a nominal intermediate frequency of 4.092 MHz, samples the resulting near-baseband signal at 4.092 MHz and digitises it with an amplitude resolution of one bit per sample. It considers only the in-phase component and discards the quadrature component.

The data collection consists of four static and seven dynamic tests under various conditions with 3700 GNSS signal snapshots in total.
We captured the 225 static snapshots on a hill top, on a bridge, in a courtyard, and in a park in 5-30 s intervals and the 3475 dynamic ones while cycling in either urban or rural environments and using 20 s intervals.
We obtained ground truth locations or tracks either by using an [Ordenance Survey trig point](https://www.ordnancesurvey.co.uk/gps/legacy-control-information/triangulation-stations) (one test), by employing satellite imagery from [Google Maps](https://www.google.com/maps) or [Google Earth](https://www.google.com/earth/) (seven tests), or with a [moto c](https://www.motorola-support.com/uk-en/?page=device/motorola/moto-c/specifications) smartphone with built-in GPS and A-GPS receiver (four tests).
While the trig point provides a ground-truth position with centimetre-level accuracy, the positions obtained from satellite imagery or with the moto c are up to 5 m wrong with outliers up to 10 m.

| dataset | size | type    | location    | ground truth          | temperatures & pressures |
|:-------:| ----:|:-------:|:-----------:|:---------------------:|:------------------------:|
| `A`     |  181 | static  | hill top    | trig point            | no                       |
| `B`     |   14 | static  | bridge      | Google Maps           | no                       |
| `C`     |    6 | static  | courtyard   | Google Maps           | no                       |
| `D`     |   24 | static  | park        | Google Maps           | yes                      |
| `E`     |  380 | dynamic | urban       | Google Earth          | yes                      |
| `F`     |  339 | dynamic | urban       | Google Earth          | yes                      |
| `G`     |  693 | dynamic | urban/rural | Google Earth          | yes                      |
| `H`     |  628 | dynamic | urban       | moto c                | yes                      |
| `I`     | 1023 | dynamic | urban/rural | Google Earth / moto c | yes                      |
| `J`     |  346 | dynamic | urban/rural | moto c                | yes                      |
| `K`     |   66 | dynamic | urban       | moto c                | yes                      |

The eleven datasets are stored in one folder per set named `A`-`K`. Each snapshot is a single binary `.bin` file with a name derived from the timestamp. One byte of the file holds the amplitude values of eight signal samples, i.e., the first byte holds the first eight samples. A zero bit represents a signal amplitude of +1 and a one bit a signal amplitude of -1. The order of the bits is 'little', i.e., reversed. For example, the byte `0b01100000` corresponds to the signal chunk `[ 1  1  1  1  1 -1 -1  1]`. In addition to the raw GNSS signal sanpshots, you can find more data in a single `meta.json` file in each folder. The `json` structs in these files provide approximate `latitude` and `longitude` of the ground truth locations of the static tests in decimal degrees, an estimate of the true `intermediate_frequency` in Hertz (the actual value differs from the nominal 4.092 MHz due to imprecissions of the hardware), all the `file` names of the binary files, the UTC `timestamp`s of all files, and optionally `temperature` and `pressure` measurements from on-board sensors in degrees Celsius or Pascal. Finally, a `.gpx` or `.kml` file provides the ground truth track for a dynamic test as a nodes of a polyline. Folder `I` contains two files that represent the first and the second part of the experiment, respectively.
