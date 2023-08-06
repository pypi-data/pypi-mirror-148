# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 11:54:36 2022

@author: PURUSHOT

Lets treat the Laue patterns as multi-blob problem with open cv
Detect multi blob locations
Then find through the image series if these blobs exists elsewhere
Do a voting system to know which blob is present where

"""
import numpy as np
import glob
import re
from tqdm import tqdm, trange
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
import itertools

try:
    from lauetools import imageprocessing as ImProc
except:
    import lauetoolsnn.lauetools.imageprocessing as ImProc

from skimage.feature import blob_log
import cv2

from vtk.util import numpy_support
import vtk

def process_images(filename):
    verbose = 0

    data_8bit_raw = plt.imread(filename)
    if verbose:
        cv2.imshow('data_8bit_raw', data_8bit_raw)
        cv2.waitKey(0)

    backgroundimage = ImProc.compute_autobackground_image(data_8bit_raw, boxsizefilter=10)
    if verbose:
        cv2.imshow('backgroundimage', backgroundimage)
        cv2.waitKey(0)

    # basic substraction
    data_8bit_rawtiff = ImProc.computefilteredimage(data_8bit_raw, 
                                                    backgroundimage, 
                                                    "sCMOS", 
                                                    usemask=True, 
                                                    formulaexpression="A-B")
    if verbose:
        cv2.imshow('backgroundimageCorrected', data_8bit_rawtiff)
        cv2.waitKey(0)
        
    data_8bit_raw = np.copy(data_8bit_rawtiff)
    ## simple thresholding
    bg_threshold = 100
    data_8bit_raw[data_8bit_raw < bg_threshold] = 0
    data_8bit_raw[data_8bit_raw > 0] = 255
    data_8bit_raw = data_8bit_raw.astype(np.uint8)
    
    ### Resize
    data_8bit_raw = cv2.resize(data_8bit_raw,(0,0),fx = 0.25, fy = 0.25)
    if verbose:
        cv2.imshow('Bin image', data_8bit_raw)
        cv2.waitKey(0)
    #Lapacian of gaussian
    data_8bit_rawtiff = cv2.resize(data_8bit_rawtiff,(0,0),fx = 0.25, fy = 0.25)
    blobs_log = blob_log(data_8bit_raw, min_sigma=1, max_sigma=15, num_sigma=30, threshold=0.01)# Compute radii in the 3rd column.
    blobs_log = blobs_log.astype(np.int64)
    blobs_log[:, 2] = data_8bit_rawtiff[blobs_log[:, 0], blobs_log[:, 1]]
    return blobs_log

def numpy_array_as_vtk_image_data(source_numpy_array, nx, ny, nz, 
                                  filename='default.vti', dtype="INT"):
    """
    Convert numpy arrays to VTK class object
    Seems to support only Log-Scale color now
    Need to check the nb of component parameters in VTK IMAGE class TODO
    """
    source_numpy_array = source_numpy_array.reshape((source_numpy_array.size))
    data_array = numpy_support.numpy_to_vtk(source_numpy_array)
    image_data = vtk.vtkImageData()
    vtkinfo = image_data.GetInformation()
    if dtype == "FLOAT":
        image_data.SetPointDataActiveScalarInfo(vtkinfo, vtk.VTK_DOUBLE, 1)
    elif dtype == "INT":
        image_data.SetPointDataActiveScalarInfo(vtkinfo, vtk.VTK_INT, 1)
    image_data.SetOrigin(0, 0, 0)
    image_data.SetSpacing(1, 1, 1)
    image_data.SetExtent(0, nx - 1, 0, ny - 1, 0, nz - 1)
    image_data.GetPointData().AddArray(data_array)
    # export data to file
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(image_data)
    writer.Write()

def extract_patch_ori_pp(results, index, lim_x, lim_y, max_len, peak_tolerance):
    peaks = results[index]
    int_sort = np.argsort(peaks[:,2])[::-1]
    peaks = peaks[int_sort]
    voting_volume = np.zeros((lim_x*lim_y, max_len), dtype=np.int64)
    for jpeak, peaks1 in enumerate(results):  
        diff = (peaks[:,None,:] - peaks1)
        # diff_intensity = -diff[:,:,2] ## +ve indicates high intensity from reference peak
        diff_position = np.abs(diff[:,:,:2]).sum(axis=2)
        diff_position_tol = diff_position < peak_tolerance
        indx, indy = np.where(diff_position_tol)
        voting_volume[jpeak,indx] = peaks1[indy,2] #diff_intensity[indx, indy]
    voting_volume = voting_volume.reshape((lim_x, lim_y, voting_volume.shape[1]))
    return voting_volume

def lower_bound_index(x, l):
    for i, y in enumerate(l):
        if y > x:
            return i
    return len(l)

# =============================================================================
# calculations
# =============================================================================

if __name__ == "__main__":
    folder_tiff = r"E:\vijaya_lauedata\HS261120b_SH2_S5_B_"
    lim_x, lim_y = 51,51
    experimental_prefix= "HS261120b_SH2_S5_B_"
    format_file = "tif"
    list_of_files = glob.glob(folder_tiff+'//'+experimental_prefix+'*.'+format_file)
    list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
    
    segment_images = False
    analyze_peaks = True
    write_vtk = False
    
    if segment_images: #30 seconds per iamge
        n_processes = cpu_count()
        args = zip(list_of_files)
        with Pool(processes=n_processes) as proc_pool:
            results = proc_pool.starmap(process_images, tqdm(args, total=len(list_of_files)))
        np.savez_compressed("npz_files"+"//"+experimental_prefix+'.npz', results)
    
    if analyze_peaks: # 5 sec per image
        results = list(np.load("npz_files"+"//"+experimental_prefix+"noresize.npz", allow_pickle=True)["arr_0"])
        peak_tolerance = 2 #pixels
        max_len = 0
        for i in results:
            if len(i) > max_len:
                max_len = len(i)
                
        # val12 = list(range(len(results)))
        val12 = list(range(1))
                
        args = zip(itertools.repeat(results), val12, itertools.repeat(lim_x),
                    itertools.repeat(lim_y), itertools.repeat(max_len), itertools.repeat(peak_tolerance))
        with Pool(processes=cpu_count()) as proc_pool:
            results_mp = proc_pool.starmap(extract_patch_ori_pp, tqdm(args, total=len(val12)))

        # results_mp_= []
        # for i in range(len(results_mp)):
        #     temp = results_mp[i].sum(axis=2)
        #     results_mp_.append(temp)      
        # results_mp_ = np.array(results_mp_)
        # results_mp_ = results_mp_.sum(axis=0)
        
        def return_intersection(hist_1, hist_2):
            # intersection of two histogram
            minima = np.minimum(hist_1, hist_2)
            intersection = np.true_divide(np.sum(minima), np.sum(hist_2))
            return intersection*100
        
        #1D histo with image index
        bin_range = lim_x * lim_y
        score = np.zeros((max_len, max_len))
        for peak_index in range(max_len):
            # histo = results_mp[image_no][:,:,peak_index].flatten()
            # h = np.histogram(list(range(bin_range)), weights=histo, bins=list(range(bin_range)))
            # plt.hist(list(range(bin_range)), weights=histo, bins=list(range(bin_range)))
            for peak_index1 in range(max_len):
                score[peak_index, peak_index1] = return_intersection(results_mp[0][:,:,peak_index].flatten(), 
                                          results_mp[0][:,:,peak_index1].flatten())
                   
        peak1_corr = np.where(score[0,:] > 75)[0]
        plt.imshow(results_mp[0][:,:,peak1_corr].sum(axis=2),origin='lower', aspect='auto',cmap='Blues')
        cb = plt.colorbar()
        cb.set_label("Intensity")
        
        
        if write_vtk:
            image_no = 0
            result_peak = results_mp[image_no]

            numpy_array_as_vtk_image_data(result_peak, 
                                          result_peak.shape[0], 
                                          result_peak.shape[1], 
                                          result_peak.shape[2],
                                          filename=experimental_prefix+'noresize.vti', 
                                          dtype="INT")
            
            # ## compare the 2D histogram of each peaks to see (TODO)
            # plt.imshow(results_mp[:,:,0],
            #             origin='lower', aspect='auto',
            #             cmap='Blues')
            # cb = plt.colorbar()
            # cb.set_label("Intensity")            
            
            
            ## We can create a box of same x,y dimension (raster scan max axis)
            ## then we split the intensity into these boxes to get a rough 3D representation
            ## Max intensity is maximum giving the surface voxels and linearly dropping 
            ## with depth
            
            peak_index = 0 # which peak; 0 is the intense peak in image
            for peak_index in range(10):
                zdim = 51
                peak_max = result_peak[:,:,peak_index].max()
                peak_min = result_peak[:,:,peak_index].min()
                step = (peak_max - peak_min)//zdim
                if step == 0:
                    step = 1
                    
                intensity_range = list(range(peak_min, peak_max, step))
        
                volume_3d = np.zeros((zdim, lim_x, lim_y), dtype=np.int8)
                for i in range(lim_x):
                    for j in range(lim_y):
                        index = lower_bound_index(result_peak[i,j,peak_index], intensity_range)
                        volume_3d[-index:,i,j] = 1
                        
                numpy_array_as_vtk_image_data(volume_3d, 
                                              volume_3d.shape[0], 
                                              volume_3d.shape[1], 
                                              volume_3d.shape[2],
                                              filename=experimental_prefix+str(peak_index)+'Volumenoresize.vti', 
                                              dtype="INT")
            
        

        
        
    
            
            