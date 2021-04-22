# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:11:44 2021

@author: Jonas Beuchert
"""
import os
import glob
import json
import numpy as np


class Dataset:
    """
    GNSS snapshot dataset representation.

    Methods
    -------
    get_size()
        Get number of snapshots in dataset, i.e., size of dataset.
    get_snapshot(idx, normalize=False)
        Get specific raw GNSS signal snapshot.
    get_ground_truth()
        Get ground truth location or track.
    get_intermediate_frequency()
        Get intermediate frequency.
    get_timestamps()
        Get all times when measurements were taken / snapshots were captured.
    get_temperatures()
        Get all temperature measurements.
    get_pressures()
        Get all pressure measurements.
    get_error(self, latitude, longitude)
        Calculate horizontal error w.r.t. ground truth point / track.

    """

    def __init__(self, directory):
        """
        Create snapshot dataset representation.

        Parameters
        ----------
        directory : string
            Dataset directory that contains the binary raw data as .bin files,
            other data as meta.json file, and potentially ground truth tracks
            as .kml or .gpx file(s).

        Returns
        -------
        None.

        """
        self._directory = directory
        # Load meta data from json file
        meta_file = os.path.join(directory, "meta.json")
        try:
            with open(meta_file, "r") as file_id:
                meta_data = json.load(file_id)
        except (ValueError, IOError):
            print(f"Cannot read data from {meta_file}.")
            return
        # Set class instance attributes
        try:
            self._intermediate_frequency = meta_data["intermediate_frequency"]
        except KeyError:
            self._intermediate_frequency = None
            print(f"No intermediate_frequency in {meta_file}.")
        try:
            self._filenames = meta_data["file"]
        except KeyError:
            self._filenames = None
            print(f"No filenames in {meta_file}.")
        try:
            self._timestamps = np.array([np.datetime64(d)
                                         for d in meta_data["timestamp"]])
        except KeyError:
            self._timestamps = None
            print(f"No timestamps in {meta_file}.")
        except ValueError():
            self._timestamps = None
            print(f"Timestamps do not match expected format in {meta_file}.")
        try:
            self._temperatures = np.array(meta_data["temperature"])
        except KeyError:
            self._temperatures = None
            print(f"No temperatures in {meta_file}.")
        try:
            self._pressures = np.array(meta_data["pressure"]).astype(float)
        except KeyError:
            self._pressures = None
            print(f"No pressures in {meta_file}.")

        # Ground truth track for dynamic dataset
        gt_files = glob.glob(os.path.join(directory, "ground_truth*"))
        if len(gt_files) > 0:
            try:
                import pymap3d as pm
                import xml.etree.ElementTree as et
                import shapely.geometry as sg
            except ImportError:
                print("Miss packages that are required to load ground truth.")
                print("Install pymap3d and Shapely.")
                return
            gt_enu = []
            for gt_file in gt_files:
                # Load ground truth
                root = et.parse(gt_file).getroot()
                file_ending = gt_file[-3:]
                print("Open ground truth file of type " + file_ending + ".")
                if file_ending == "gpx":
                    # Ground truth track as list of polyline nodes
                    self._ground_truth = [{
                        "latitude": float(child.attrib['lat']),
                        "longitude": float(child.attrib['lon'])
                        } for child in root[-1][-1]]
                elif file_ending == "kml":
                    # Get coordinates of path
                    try:
                        gt_string = root[-1][-1][-1][-1][-1][-1].text
                    except(IndexError):
                        gt_string = root[-1][-1][-1][-1].text
                    gt_geo = np.fromstring(
                        gt_string.replace('\n', '').replace('\t', '').replace(
                            ' ', ','), sep=',')
                    # Ground truth track as list of polyline nodes
                    self._ground_truth = [{"latitude": lat,
                                           "longitude": lon}
                                          for lat, lon
                                          in zip(gt_geo[1::3], gt_geo[::3])]
                else:
                    raise ValueError(
                        "Ground truth file format {} not recognized.".format(
                            file_ending))

                # Transform to ENU coordinates with same reference
                self._ref_location = self._ground_truth[0]
                gt_enu.append(np.array(pm.geodetic2enu(
                    [g["latitude"] for g in self._ground_truth],
                    [g["longitude"] for g in self._ground_truth], 0,
                    self._ref_location["latitude"],
                    self._ref_location["longitude"], 0)).T)
            # Concatenate both parts, if there are two
            gt_enu = np.vstack(gt_enu)
            # Convert to line
            self._track = sg.LineString([(p[0], p[1]) for p in gt_enu])
        else:
            try:
                self._ground_truth = {
                    "latitude": meta_data["latitude"],
                    "longitude": meta_data["longitude"]}
            except KeyError:
                self._ground_truth = None
                print(f"No ground truth file in {directory}.")
                print(f"No ground truth location in {meta_file}.")
            self._ref_location = self._ground_truth
            self._track = None

    def get_size(self):
        """
        Get number of snapshots in dataset, i.e., size of dataset.

        Returns
        -------
        int
            Number of snapshots in dataset.

        """
        return len(self._filenames)

    def get_snapshot(self, idx, normalize=False):
        """
        Get specific raw GNSS signal snapshot.

        Parameters
        ----------
        idx : int
            Index of file / snapshot.
        normalize : bool, optional
            Subtract mean from signal. The default is False.

        Returns
        -------
        np.ndarray, dtype=int8 if normalize=False, dtype=float32 if
        normalize=True, shape=(49104,)
            Binary raw GNSS snapshot with length 12 ms sampled at 4.092 MHz.
            Samples element of {-1, +1} if normalize=False.
            DC component removed, i.e., mean subtracted if normalize=True.

        """
        try:
            filename = os.path.join(self._directory, self._filenames[idx])
        except IndexError:
            print(
                f"Snapshot index {idx} out of range {0}-{self.get_size()-1}.")
            return None
        # Read signals from files
        # How many bytes to read
        bytes_per_snapshot = int(4092000.0 * 12e-3 / 8)
        # Read binary raw data from file
        signal_bytes = np.fromfile(filename, dtype='>u1',
                                   count=bytes_per_snapshot)
        # Get bits from bytes
        signal = np.unpackbits(signal_bytes, axis=-1, count=None,
                               bitorder='little')
        # Convert snapshots from {0,1} to {-1,+1}
        signal = -2 * signal.astype(np.int8) + 1
        # Check if signal shall be normalized
        if normalize:
            signal = signal.astype(np.float32)
            return signal - np.mean(signal)
        return signal

    def get_ground_truth(self):
        """
        Get ground truth location or track.

        Returns
        -------
        dict {"latitude": float, "longitude": float}
        or list of dict {"latitude": float, "longitude": float}
            Dictionary with static ground truth location or list of
            dictionaries for ground truth track. The list defines a polyline,
            which nodes are not directly related to snapshots.

        """
        return self._ground_truth

    def get_intermediate_frequency(self):
        """
        Get intermediate frequency.

        Returns
        -------
        float
            Intermediate frequency [Hz].

        """
        return self._intermediate_frequency

    def get_timestamps(self):
        """
        Get all times when measurements were taken / snapshots were captured.

        Returns
        -------
        numpy.ndarray, dtype=numpy.datetime64[ms], shape=(N,)
            Timestamps in UTC.

        """
        return self._timestamps

    def get_temperatures(self):
        """
        Get all temperature measurements.

        Returns
        -------
        numpy.ndarray, dtype=float64, shape=(N,)
            List of ambient temperatures [°C].

        """
        return self._temperatures

    def get_pressures(self):
        """
        Get all pressure measurements.

        Returns
        -------
        numpy.ndarray, dtype=float64, shape=(N,)
            List of ambient pressures [Pa].

        """
        return self._pressures

    def get_error(self, latitude, longitude):
        """
        Calculate horizontal error w.r.t. ground truth point / track.

        Parameters
        ----------
        latitude : float
            Latitude of test location [°].
        longitude : float
            Longitude of test location [°].

        Returns
        -------
        float
            Horizontal (2D) Euclidean distance [m] between test location and
            ground truth location / or next location on ground truth track.

        """
        try:
            import pymap3d as pm
        except ImportError:
            print("Miss package that is required to calculate error.")
            print("Install pymap3d.")
            return
        # Calculate positioning error in ENU coordinates [m,m,m]
        err_east, err_north, err_height \
            = pm.geodetic2enu(latitude, longitude, 0,
                              self._ref_location["latitude"],
                              self._ref_location["longitude"], 0)

        if self._track is not None:
            try:
                import shapely.geometry as sg
            except ImportError:
                print("Miss package that is required to calculate error.")
                print("Install Shapely.")
                return
            pos_enu = np.array([err_east, err_north, err_height])
            # Get nearest point on line for all estimated points
            nearest_point = self._track.interpolate(self._track.project(
                sg.Point((pos_enu[0], pos_enu[1]))
                ))

            # Calculate horizontal error
            err = np.linalg.norm(nearest_point.coords[0] - pos_enu[:2])
        else:
            err = np.linalg.norm(np.array([err_east, err_north]))

        if np.isnan(err):
            return np.inf
        else:
            return err
