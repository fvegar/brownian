# -*- coding: utf-8 -*-
"""
Created on Sat May  2 19:56:44 2020

@author: malopez
"""
import sys
import cv2
import os
import pims
import multiprocessing as mp
from functools import partial
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from tqdm import tqdm
from scipy.signal import savgol_filter, find_peaks
from utils import createCircularMask, maskImage, angle_from_2D_points


def get_radial_brightness_peaks(video_path, row, min_r=15, max_r=20):
    indice = int(row[0])
    frame_number = int(row[1])
    x = row[2]
    y = row[3]
    video = pims.Cine(video_path)
    frame = video.get_frame(frame_number-1)
    # Select only the portion of the frame corresponfing to current particle (x,y)
    # And mask so that only an annulus is visible (corresponding to the 'aspas')
    outer_mask = createCircularMask(800, 1280, center=[x,y], radius=max_r)
    inner_mask = createCircularMask(800, 1280, center=[x,y], radius=min_r)
    frame = maskImage(frame, outer_mask)
    frame = maskImage(frame, ~inner_mask)

    df = pd.DataFrame(frame)
    df['y'] = df.index
    df = pd.melt(df, id_vars=[('y')])
    df.rename(columns = {'variable':'x', 'value':'brightness'}, inplace = True)
    df = df[df.brightness!=0]
    df['brightness'] *= (255/frame.max())

    x_rel_to_center = df['x'] - x
    y_rel_to_center = df['y'] - y
    #df['angles'] = angle_from_2D_points(x_rel_to_center.astype(int).values, y_rel_to_center.astype(int).values)
    df['angles'] = angle_from_2D_points(x_rel_to_center.astype(float).values, y_rel_to_center.astype(float).values)
    df.sort_values('angles', inplace=True)

    angulos = df['angles'].values
    new_angulos = np.append(angulos,angulos[:100]+360)
    brillo = savgol_filter(df['brightness'], window_length=21, polyorder=3)
    new_brillo = np.append(brillo,brillo[:100])
    
    picos_indice, picos_altura = find_peaks(new_brillo, distance=int(len(new_brillo)/24.),width=5, prominence=5)
    picos = new_angulos[picos_indice]
    
    if picos[0] == 0.: 
        picos = np.delete(picos,0,0)
    
    dips_indice, dips_altura = find_peaks(-new_brillo, distance=int(len(new_brillo)/24.),width=5, prominence=5)
    
    dips = new_angulos[dips_indice]
    
    if dips[0] == 0.:
        dips = np.delete(dips,0,0)

    return (indice, [picos, dips])



def detect_brightness_maxima(file, data_file):
    # GRADOS_POR_ASPA = 360/14.
    video_path = file
    df = pd.read_pickle(data_file, compression='xz')#[:lengthy]
    df['indice'] = df.index

    # Función parcial, ahora solo acepta como entrada una lista, de la forma [indice, n_frame, x, y]
    partial_get_peaks = partial(get_radial_brightness_peaks, video_path, min_r=15, max_r=20)

    rows = df[['indice','frame','x','y']].values#[:lengthy]
    N = len(rows)

    # Calculamos los angulos de los picos de brillo alrededor de las partículas.
    # Usamos múltiples procesadores
    N_CORES = mp.cpu_count()
    print(f'Computing angular brightness peaks using {N_CORES} cores \n')
    with mp.Pool(processes=N_CORES) as pool:
        dict_indices_max_mins = dict(list(tqdm(pool.imap(partial_get_peaks, rows), total=N)))
       
    df['extremos'] = df['indice'].map(dict_indices_max_mins)

    return df