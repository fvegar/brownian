# -*- coding: utf-8 -*-
"""
Created on Sat May  2 19:56:44 2020

@author: malopez 
@author: Alejandro Márquez Seco
"""
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
import os


def calculate_angular_velocity(df):
    GRADOS_POR_ASPA = 360./14
    df['indice'] = df.index
        
    # df=df[:5100]  
    subs=[]
    for t in set(df['track']):
        sub = df[df['track']==t]
        angles_column=[]
        picos_array=(sub['extremos'])
        
        negative_values=0
        saltos = 0
        for frame in range(0,len(picos_array)): # Loop over each frame
            if frame>0:   # Calcula el ángulo sólo para los frames superiores a 1
            
                picos_now = picos_array.iloc[frame][0]
                dips_now = picos_array.iloc[frame][1]
                picos_past = picos_array.iloc[(frame-1)][0]
                dips_past = picos_array.iloc[(frame-1)][1]
                
                angles_reg_pic=[]
                angles_reg_dip=[]
                angles_prev_pic=[]
                angles_prev_dip=[]
                angles_next_pic=[]
                angles_next_dip=[]
                cambio_pics_now = 0
                cambio_dips_now = 0
                cambio_pics_past = 0 
                cambio_dips_past = 0         
                cambio_pic_now = False    
                cambio_pic_past = False
                cambio_dip_now = False
                cambio_dip_past = False
                pos_cambio_pic_past = 18
                pos_cambio_dip_past = 18
                pos_cambio_pic_now = 18
                pos_cambio_dip_now = 18
                for i in range(1,15):  
    # Las siguientes líneas calculan si hay algún máximo o mínimo que no se ha detectado
    # Si ese es el caso, se salta ese cálculo (se aumenta el índice)
                    if cambio_pic_past == False: # Si no se ha detectado ningún cambio de índice, se busca
                        if round(np.abs(picos_now[i] -picos_now[i-1])/GRADOS_POR_ASPA)  == 2:
                            cambio_pics_past = 1  # falta un máximo en picos_now, se aumenta el índice de picos_past, se salta un pico en picos_past
                            cambio_pic_past = True
                            pos_cambio_pic_past = i
                            
                        if  round(np.abs(picos_past[i] - picos_past[i-1])/GRADOS_POR_ASPA) == 0 :
                            cambio_pics_past = 1 # sobra un máximo en picos_past, dos máximos muy cercanos
                            cambio_pic_past = True
                            pos_cambio_pic_past = i - 1  
                            
                    if cambio_pic_now == False: # Si no se ha detectado ningún cambio de índice, se busca                 
                        if round(np.abs(picos_now[i] -picos_now[i-1])/GRADOS_POR_ASPA)  == 0 :
                            cambio_pics_now = 1  # sobra un máximo en picos_now, se aumenta el índice de picos_now, se salta un pico en picos_now
                            cambio_pic_now = True
                            pos_cambio_pic_now = i - 1 
                            
                        if  round(np.abs(picos_past[i] - picos_past[i-1])/GRADOS_POR_ASPA) == 2 :
                            cambio_pics_now = 1 # falta un máximo en picos_past
                            cambio_pic_now = True
                            pos_cambio_pic_now = i
                        
                           
                    if cambio_dip_past == False:    
                        if round(np.abs(dips_now[i] - dips_now[i-1])/GRADOS_POR_ASPA) == 2 :
                            cambio_dips_past = 1
                            cambio_dip_past == True 
                            pos_cambio_dip_past = i 
                        if  round(np.abs(dips_past[i] - dips_past[i-1])/GRADOS_POR_ASPA)  == 0 :
                            cambio_dips_past = 1
                            cambio_dip_past == True
                            pos_cambio_dip_past = i 
                                           
                    if cambio_dip_now == False:   
                        if round(np.abs(dips_now[i] - dips_now[i-1])/GRADOS_POR_ASPA) == 0 :
                            cambio_dips_now = 1
                            cambio_dip_now == True
                            pos_cambio_dip_now = i 
                        if  round(np.abs(dips_past[i] - dips_past[i-1])/GRADOS_POR_ASPA)  == 2 :
                            cambio_dips_now = 1
                            cambio_dip_now == True
                            pos_cambio_dip_now = i
                rango = 14            
                if cambio_dip_now == True or cambio_dip_past == True or cambio_pic_now == True or cambio_pic_past == True:
                    rango=  13         
                for i in range(0,rango):  # Calcula la separación entre picos con la misma etiqueta
                     # Se modifica el índice de los máximos después del valor detectado como cambio
                    
                    indice_dip_now = i
                    indice_dip_past = i
                    indice_dip_now_adelantado = i + 1
                    indice_dip_past_adelantado = i + 1
                    
                    if indice_dip_now_adelantado >= pos_cambio_dip_now:
                        indice_dip_now_adelantado = i + 2
                    if indice_dip_past_adelantado >= pos_cambio_dip_past:
                        indice_dip_past_adelantado = i + 2
                    if i >= pos_cambio_dip_now:
                        indice_dip_now = i+cambio_dips_now
                    if i >= pos_cambio_dip_past:     
                        indice_dip_past = i+cambio_dips_past
                        
                        
                    indice_pic_now = i
                    indice_pic_past = i
                    indice_pic_now_adelantado = i+1
                    indice_pic_past_adelantado = i+1
                    
                    if indice_pic_past_adelantado >= pos_cambio_pic_past:
                        indice_pic_past_adelantado= i + 2
                    if indice_pic_now_adelantado >= pos_cambio_pic_now:
                        indice_pic_now_adelantado= i + 2
                    if i >= pos_cambio_pic_now:
                        indice_pic_now = i+cambio_pics_now
                    if i >= pos_cambio_pic_past:
                        indice_pic_past = i+cambio_pics_past
                        
                        
                # Angle difference for peaks and dips with the same index    
                    dif_pic_reg = picos_past[indice_pic_past] - picos_now[indice_pic_now] 
                    dif_dip_reg = dips_past[indice_dip_past] - dips_now[indice_dip_now]
                    angles_reg_pic.append(dif_pic_reg)
                    angles_reg_dip.append(dif_dip_reg)
 
                   # Angle difference for peaks and dips with the index difference -1  
                    if len(picos_now) > indice_pic_now_adelantado and len(picos_past)>indice_pic_past:
                        dif_pic_prev = picos_past[indice_pic_past] - picos_now[indice_pic_now_adelantado]
                        angles_prev_pic.append(dif_pic_prev)
                    if len(dips_now) > indice_dip_now_adelantado and len(dips_past)>indice_dip_past:  
                        dif_dip_prev = dips_past[indice_dip_past] - dips_now[indice_dip_now_adelantado]
                        angles_prev_dip.append(dif_dip_prev)
                    
                   # Angle difference for peaks and dips with the index difference +1  
                    if len(picos_past)>indice_pic_past_adelantado and len(picos_now)>indice_pic_now:
                        dif_pic_next =  picos_past[indice_pic_past_adelantado] - picos_now[indice_pic_now]
                        angles_next_pic.append(dif_pic_next)
                    if len(dips_past)>indice_dip_past_adelantado and len(dips_now)>indice_dip_now:
                        dif_dip_next = dips_past[indice_dip_past_adelantado] -  dips_now[indice_dip_now]
                        angles_next_dip.append(dif_dip_next)
                    
                avg_reg_pic=np.mean(angles_reg_pic) 
                avg_reg_dip=np.mean(angles_reg_dip) 
                               
                avg_prev_pic=np.mean(angles_prev_pic) 
                avg_prev_dip=np.mean(angles_prev_dip) 
                        
                avg_next_pic=np.mean(angles_next_pic) 
                avg_next_dip=np.mean(angles_next_dip) 
                
                pic_angles =[angles_reg_pic, angles_prev_pic, angles_next_pic]
                dip_angles =[angles_reg_dip, angles_prev_dip, angles_next_dip]
                
                avg_pic_angles =[avg_reg_pic, avg_prev_pic, avg_next_pic]
                avg_dip_angles =[avg_reg_dip, avg_prev_dip, avg_next_dip]
                
                abs_pic_angles =[np.abs(avg_reg_pic), np.abs(avg_prev_pic), np.abs(avg_next_pic)]
                abs_dip_angles =[np.abs(avg_reg_dip), np.abs(avg_prev_dip), np.abs(avg_next_dip)]
                
                for angly in range(0,len(avg_dip_angles)):
                    if np.amin(abs_dip_angles) == np.abs(avg_dip_angles[angly]):
                        real_dip_angle = avg_dip_angles[angly]
                        real_dip_angles = dip_angles[angly]
                for angly in range(0,len(avg_pic_angles)):
                    if np.amin(abs_pic_angles) == np.abs(avg_pic_angles[angly]):
                        real_pic_angle = avg_pic_angles[angly]
                        real_pic_angles = pic_angles[angly]
                real_angle =np.mean([real_pic_angle , real_dip_angle])
                angles_column.append(real_angle)
                
                if cambio_dip_now == True or cambio_dip_past == True or cambio_pic_now == True or cambio_pic_past == True:
                    saltos +=1
                if real_angle < 0:
                    
                    negative_values+=1
                
            else: 
                # Only for the first frame, the velocity is copied from the second frame
                angles_column.append(np.nan) 
                
        if len(angles_column)>=2:
            angles_column[0]=angles_column[1]
        
        sub['angular_velocity']=angles_column
        subs.append(sub)
        
    new_df = pd.concat(subs, axis=0)
    print(f'Negative angles: {negative_values}')
    print(f'Saltos: {saltos}')

    return new_df



    
# =============================================================================
#     anglesss = (new_df['angles'])
#     cleanedList = [x for x in anglesss if str(x) != 'nan']
#     df.to_pickle(os.path.join(folder, str(experiment_id)+'_giros_ale.pkl'), compression='xz')
#     
#     plt.hist(cleanedList, bins=125)
#     plt.savefig(os.path.join(folder, str(experiment_id)+'_histogram.png'))
#     plt.plot()
#     plt.close()
# =============================================================================
