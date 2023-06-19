from tkinter import *
from tkinter import ttk
import csv
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog as fd
import plotly.graph_objs as go
from math import *
import os
import pandas as pd
import numpy as np

window_main = Tk()
window_main.title ('Drilling complications on the trajectory')
window_main.geometry ('640x400')
window_main.resizable(False, False)

bg1='gainsboro' 
bg2='rosybrown'
bg3='darkgray'
font1='Arial 9 bold'
font2='Arial 9' 

up_frame  =  Frame(window_main,  width=90,  height=  400,  bg=bg1)
up_frame.grid(row=0,  column=0,  padx=1,  pady=1, sticky='w'+'e'+'n'+'s')
mid_frame  =  Frame(window_main,  width=90,  height=  400,  bg=bg3)
mid_frame.grid(row=1,  column=0,  padx=1,  pady=1, sticky='w'+'e'+'n'+'s')
down_frame  =  Frame(window_main,  width=90,  height= 420,  bg=bg2)
down_frame.grid(row=2,  column=0,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
#---------------------------------------------------------------------------------------------
directory_to_trajectory = ""
well = pd.DataFrame()

def open_directory_to_trajectory():
    global directory_to_trajectory, well 
    directory_to_trajectory = fd.askopenfilename()
    well = pd.read_excel(directory_to_trajectory)
    text_0=well.head()
    text_1=well.tail()
    text_2=well.info()
    st.insert(END, str(directory_to_trajectory) + '\n')
    st.insert(END, str(text_0) + '\n')
    st.insert(END, '* * *' + '\n')
    st.insert(END, str(text_1) + '\n')
    st.insert(END, str(text_2) + '\n')
    st.see('end')
    return well
#---------------------------------------------------------------------------------------------
def trajectory_build_function():
    global well
    well.at[0, 'north'] = 0
    well.at[0, 'east'] = 0
    well.at[0, 'TVD'] = 0
    well_name = well_name_entry.get()
    #Построение траектории ствола
    for index, row in well.iterrows():
        if index > 0:
            inc1 = well.at[index - 1, 'incl']
            inc2 = row ['incl']
            azi1 = well.at[index - 1, 'azi']
            azi2 = row['azi']          
            md1 = well.at[index - 1, 'MD']
            md2 = row['MD']
            delta_md = md2 - md1
            Di_za_10m = (10 * (inc2 - inc1)) / (md2 - md1)
            Betta_dog_leg_angle = acos (cos(inc2-inc1) - (sin(inc1) * sin(inc2) * (1-cos(azi2-azi1))))
            
            if Di_za_10m == 0:
                rf = 1
            else:
                rf = tan(0.5 * Di_za_10m) / (Di_za_10m * 0.5)

            if inc1 == inc2:
                tvd_delta = delta_md * cos(radians(inc2))
            else:
                tvd_delta = (573 / Di_za_10m) * (sin (radians(inc2))-sin(radians(inc1)))

            tvd = tvd_delta + well.at[index-1, 'TVD']
            north_delta = 0.5 * delta_md * (sin(radians(inc1)) * cos(radians(azi1))
                                        + sin(radians(inc2)) * cos(radians(azi2))) * rf
            north = north_delta + well.at[index-1, 'north']

            east_delta = 0.5 * delta_md * (sin(radians(inc1)) * sin(radians(azi1))
                                    + sin(radians(inc2)) * sin(radians(azi2))) * rf
            east = east_delta + well.at[index-1, 'east']

            well.at[index, 'd_MD'] = delta_md
            well.at[index, 'dl'] = Betta_dog_leg_angle
            well.at[index, 'RF'] = rf
            well.at[index, 'north_delta'] = north_delta
            well.at[index, 'east_delta'] = east_delta
            well.at[index, 'east'] = east
            well.at[index, 'north'] = north
            well.at[index, 'TVD'] = tvd

    well_trajectory = go.Figure(data=[go.Scatter3d(x=well['north'], y=well['east'], z=well['TVD'], mode='lines', name=well_name)])

    # Настройка меток осей и заголовка
    well_trajectory.update_layout(scene=dict(xaxis_title='north', xaxis=dict(autorange='reversed'), yaxis_title='east', yaxis=dict(autorange='reversed'), zaxis_title='TVD', zaxis=dict(autorange='reversed',range=[3000, 0])), title=well_name)
    customdata_str = well[['MD', 'incl', 'azi']].astype(str).values

    well_trajectory.update_traces(
    customdata=customdata_str,
    hovertemplate='MD: %{customdata[0]}<br> TVD: %{z}<br> incl: %{customdata[1]}<br> azi: %{customdata[2]}<br> <extra></extra>'
)
    # Создание нового DataFrame с столбцом MD от 0 до заданной глубины с шагом 1
    Total_depth = int(well.at[well.index[-1], 'MD'])
    md_range = list(range(0, Total_depth + 1, 1))
    well_interpolate = pd.DataFrame({'MD': md_range})
    # Объединение DataFrame по столбцу MD и интерполяция пропущенных значений
    well_interpolate = pd.merge(well_interpolate, well, on='MD', how='left')
    well_interpolate = well_interpolate.interpolate(method='linear', axis=0)
#________________________________________________ 
    #выбор типа маркера
    symbol_of_event_1 = 'cross' 
    if symbol_1.get() == 'circle':
        symbol_of_event_1 = 'circle'
    elif symbol_1.get() == 'square':
        symbol_of_event_1 = 'square'
    elif symbol_1.get() == 'diamond':
        symbol_of_event_1 = 'diamond'
    else:
        symbol_of_event_1 = 'cross'

    symbol_of_event_2 = 'cross' 
    if symbol_2.get() == 'circle':
        symbol_of_event_2 = 'circle'
    elif symbol_2.get() == 'square':
        symbol_of_event_2 = 'square'
    elif symbol_2.get() == 'diamond':
        symbol_of_event_2 = 'diamond'
    else:
        symbol_of_event_2 = 'cross'

    symbol_of_event_3 = 'cross' 
    if symbol_3.get() == 'circle':
        symbol_of_event_3 = 'circle'
    elif symbol_3.get() == 'square':
        symbol_of_event_3 = 'square'
    elif symbol_3.get() == 'diamond':
        symbol_of_event_3 = 'diamond'
    else:
        symbol_of_event_3 = 'cross'  

    symbol_of_event_4 = 'cross' 
    if symbol_4.get() == 'circle':
        symbol_of_event_4 = 'circle'
    elif symbol_4.get() == 'square':
        symbol_of_event_4 = 'square'
    elif symbol_4.get() == 'diamond':
        symbol_of_event_4 = 'diamond'
    else:
        symbol_of_event_4 = 'cross'

    symbol_of_event_5 = 'cross' 
    if symbol_5.get() == 'circle':
        symbol_of_event_5 = 'circle'
    elif symbol_5.get() == 'square':
        symbol_of_event_5 = 'square'
    elif symbol_5.get() == 'diamond':
        symbol_of_event_5 = 'diamond'
    else:
        symbol_of_event_5 = 'cross'                                  
#________________________________________________ 
    #Отображение точек на траектории
    short_description_1_v = short_description_1.get()
    short_description_2_v = short_description_2.get()
    short_description_3_v = short_description_3.get()
    short_description_4_v = short_description_4.get()
    short_description_5_v = short_description_5.get()

    if depth_type_1var.get() == 1:
        try:
            point_of_interval_up_1 = float(Depth_entry_1_1.get())
            point_of_interval_down_1 = float(Depth_entry_1_2.get())
            x_of_interval_1 = list()
            y_of_interval_1 = list()
            z_of_interval_1 = list()

            for i in np.arange(point_of_interval_up_1, point_of_interval_down_1, 1.0):
                x_point_of_interval = [well_interpolate.at[i, 'north']]
                y_point_of_interval = [well_interpolate.at[i, 'east']]
                z_point_of_interval = [well_interpolate.at[i, 'TVD']]
                x_of_interval_1.extend(x_point_of_interval)
                y_of_interval_1.extend(y_point_of_interval)
                z_of_interval_1.extend(z_point_of_interval)

            drop_interval_1 = go.Scatter3d(x=x_of_interval_1,y=y_of_interval_1,z=z_of_interval_1, name=short_description_1_v, mode='lines',  line=dict(color='red', width=5))
            well_trajectory.add_trace(drop_interval_1)
        except ValueError:
            point_of_interval_up_1 = 0
            point_of_interval_down_1 = 0

    else:        
        try:
            depth_of_trouble_1 = float(Depth_entry_1_1.get())
            x_point_1 = [well_interpolate.at[depth_of_trouble_1,'north']] 
            y_point_1 = [well_interpolate.at[depth_of_trouble_1,'east']]
            z_point_1 = [well_interpolate.at[depth_of_trouble_1,'TVD']]
            drop_point_1 = go.Scatter3d(x=x_point_1, y=y_point_1, z=z_point_1, mode='markers', name=short_description_1_v, marker=dict(size=5,color='red', symbol=symbol_of_event_1))
            well_trajectory.add_trace(drop_point_1)
        except ValueError:
            depth_of_trouble_1 = 0
#________________________________________________    
    if depth_type_2var.get() == 1:
        try:
            point_of_interval_up_2 = float(Depth_entry_2_1.get())
            point_of_interval_down_2 = float(Depth_entry_2_2.get())
            x_of_interval_2 = list()
            y_of_interval_2 = list()
            z_of_interval_2 = list()

            for i in np.arange(point_of_interval_up_2, point_of_interval_down_2, 1.0):
                x_point_of_interval = [well_interpolate.at[i, 'north']]
                y_point_of_interval = [well_interpolate.at[i, 'east']]
                z_point_of_interval = [well_interpolate.at[i, 'TVD']]
                x_of_interval_2.extend(x_point_of_interval)
                y_of_interval_2.extend(y_point_of_interval)
                z_of_interval_2.extend(z_point_of_interval)

            drop_interval_2 = go.Scatter3d(x=x_of_interval_2, y=y_of_interval_2, z=z_of_interval_2, name=short_description_2_v,  mode='lines',  line=dict(color='red', width=5))
            well_trajectory.add_trace(drop_interval_2) 
        except ValueError:
            point_of_interval_up_2 = 0
            point_of_interval_down_2 = 0    
    else:           
        try:  
            depth_of_trouble_2 = float(Depth_entry_2_1.get())
            x_point_2 = [well_interpolate.at[depth_of_trouble_2,'north']] 
            y_point_2 = [well_interpolate.at[depth_of_trouble_2,'east']]
            z_point_2 = [well_interpolate.at[depth_of_trouble_2,'TVD']]
            drop_point_2 = go.Scatter3d(x=x_point_2, y=y_point_2, z=z_point_2, name=short_description_2_v, mode='markers',marker=dict(size=5,color='red', symbol=symbol_of_event_2))
            well_trajectory.add_trace(drop_point_2)
        except ValueError:
            depth_of_trouble_2 = 0
#________________________________________________        
    if depth_type_3var.get() == 1:
        try:
            point_of_interval_up_3 = float(Depth_entry_3_1.get())
            point_of_interval_down_3 = float(Depth_entry_3_2.get())
            x_of_interval_3 = list()
            y_of_interval_3 = list()
            z_of_interval_3 = list()

            for i in np.arange(point_of_interval_up_3, point_of_interval_down_3, 1.0):
                x_point_of_interval = [well_interpolate.at[i, 'north']]
                y_point_of_interval = [well_interpolate.at[i, 'east']]
                z_point_of_interval = [well_interpolate.at[i, 'TVD']]
                x_of_interval_3.extend(x_point_of_interval)
                y_of_interval_3.extend(y_point_of_interval)
                z_of_interval_3.extend(z_point_of_interval)

            drop_interval_3 = go.Scatter3d(x=x_of_interval_3, y=y_of_interval_3, z=z_of_interval_3, name=short_description_3_v, mode='lines',  line=dict(color='red', width=5))
            well_trajectory.add_trace(drop_interval_3) 
        except ValueError:
            point_of_interval_up_3 = 0
            point_of_interval_down_3 = 0
    else:
        try:
            depth_of_trouble_3 = float(Depth_entry_3_1.get())
            x_point_3 = [well_interpolate.at[depth_of_trouble_3,'north']] 
            y_point_3 = [well_interpolate.at[depth_of_trouble_3,'east']]
            z_point_3 = [well_interpolate.at[depth_of_trouble_3,'TVD']]
            drop_point_3 = go.Scatter3d(x=x_point_3, y=y_point_3, z=z_point_3, name=short_description_3_v, mode='markers',marker=dict(size=5,color='red', symbol=symbol_of_event_3))
            well_trajectory.add_trace(drop_point_3)
        except ValueError:
            depth_of_trouble_3 = 0
#________________________________________________                 
    if depth_type_4var.get() == 1:
        try:
            point_of_interval_up_4 = float(Depth_entry_4_1.get())
            point_of_interval_down_4 = float(Depth_entry_4_2.get())
            x_of_interval_4 = list()
            y_of_interval_4 = list()
            z_of_interval_4 = list()

            for i in np.arange(point_of_interval_up_4, point_of_interval_down_4, 1.0):
                x_point_of_interval = [well_interpolate.at[i, 'north']]
                y_point_of_interval = [well_interpolate.at[i, 'east']]
                z_point_of_interval = [well_interpolate.at[i, 'TVD']]
                x_of_interval_4.extend(x_point_of_interval)
                y_of_interval_4.extend(y_point_of_interval)
                z_of_interval_4.extend(z_point_of_interval)

            drop_interval_4 = go.Scatter3d(x=x_of_interval_4,y=y_of_interval_4,z=z_of_interval_4, name=short_description_4_v, mode='lines',  line=dict(color='red', width=5))
            well_trajectory.add_trace(drop_interval_4) 
        except ValueError:
            point_of_interval_up_4 = 0
            point_of_interval_down_4 = 0
    else:        
        try:
            depth_of_trouble_4 = float(Depth_entry_4_1.get())
            x_point_4 = [well_interpolate.at[depth_of_trouble_4,'north']] 
            y_point_4 = [well_interpolate.at[depth_of_trouble_4,'east']]
            z_point_4 = [well_interpolate.at[depth_of_trouble_4,'TVD']]
            drop_point_4 = go.Scatter3d(x=x_point_4, y=y_point_4, z=z_point_4, name=short_description_4_v, mode='markers',marker=dict(size=5,color='red', symbol=symbol_of_event_4))
            well_trajectory.add_trace(drop_point_4)
        except ValueError:
            depth_of_trouble_4 = 0
#________________________________________________             
    if depth_type_5var.get() == 1:
        try:
            point_of_interval_up_5 = float(Depth_entry_5_1.get())
            point_of_interval_down_5 = float(Depth_entry_5_2.get())
            x_of_interval_5 = list()
            y_of_interval_5 = list()
            z_of_interval_5 = list()

            for i in np.arange(point_of_interval_up_5, point_of_interval_down_5, 1.0):
                x_point_of_interval = [well_interpolate.at[i, 'north']]
                y_point_of_interval = [well_interpolate.at[i, 'east']]
                z_point_of_interval = [well_interpolate.at[i, 'TVD']]
                x_of_interval_5.extend(x_point_of_interval)
                y_of_interval_5.extend(y_point_of_interval)
                z_of_interval_5.extend(z_point_of_interval)

            drop_interval_5 = go.Scatter3d(x=x_of_interval_5, y=y_of_interval_5, z=z_of_interval_5, name=short_description_5_v, mode='lines',  line=dict(color='red', width=5))
            well_trajectory.add_trace(drop_interval_5) 
        except ValueError:
            point_of_interval_up_5 = 0
            point_of_interval_down_5 = 0
    else:        
        try:    
            depth_of_trouble_5 = float(Depth_entry_5_1.get())
            x_point_5 = [well_interpolate.at[depth_of_trouble_5,'north']] 
            y_point_5 = [well_interpolate.at[depth_of_trouble_5,'east']]
            z_point_5 = [well_interpolate.at[depth_of_trouble_5,'TVD']]
            drop_point_5 = go.Scatter3d(x=x_point_5, y=y_point_5, z=z_point_5, name=short_description_5_v, mode='markers', marker=dict(size=5,color='red', symbol=symbol_of_event_5))
            well_trajectory.add_trace(drop_point_5)
        except ValueError:
            depth_of_trouble_5 = 0    

    # 'circle'
    # 'square'
    # 'diamond'
    # 'cross'


    well_trajectory.show()
    return

#---------------------------------------------------------------------------------------------

symbol_of_event = ('circle', 'square', 'diamond', 'cross')

Label(up_frame, text='Select file path...', bg=bg1, font=font1, width=20).grid(row=1, column=1)
Button(up_frame, text="Open", font=font1, command=open_directory_to_trajectory, width=15).grid(row=1, column=2)
Label(up_frame, text='Input of well name:       ', bg=bg1, font=font1).grid(padx=10, row=1, column=3)
well_name_entry = ttk.Entry(up_frame, width=35)
well_name_entry.grid(row=1, column=4)
#---------------------------------------------------------------------------------------------
#Ввод точек внимания
#Первая точка-интервал
Label(mid_frame, text='1. ', font=font1, bg=bg3).grid(row=1, column=0, padx=0,  pady=0, sticky='w')
symbol_1 = ttk.Combobox(mid_frame, values=symbol_of_event, width=5)
symbol_1.grid(row=1, column=1, padx=0,  pady=0, sticky='e')

def flag_depth_1_type():
    if depth_type_1var.get() == 1:
        Depth_entry_1_2.configure(state=ACTIVE) 
    else:
        Depth_entry_1_2.configure(state=DISABLED) 
    return  

depth_type_1var = IntVar(value=0)
depth_type_1 = Checkbutton(mid_frame, text="Interval", bg=bg1, background=bg3, command=flag_depth_1_type, variable=depth_type_1var, activebackground=bg3, font=font2)
depth_type_1.grid(row=1, column=2)
Label(mid_frame, text='Depth, m', font=font1, bg=bg3).grid(row=1, column=3)
Depth_entry_1_1 = ttk.Entry(mid_frame, width=5) 
Depth_entry_1_1.grid(row=1, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text=' - ', bg=bg3).grid(row=1, column=5)
Depth_entry_1_2 = ttk.Entry(mid_frame, width=5, state=DISABLED) 
Depth_entry_1_2.grid(row=1, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text='Short Description: ', font=font1, bg=bg3).grid(row=1, column=7)
short_description_1 = ttk.Entry(mid_frame, width=35) 
short_description_1.grid(row=1, column=8, padx=1, pady=5, sticky='w')

#Вторая точка-интервал
Label(mid_frame, text='2. ', font=font1, bg=bg3).grid(row=2, column=0, padx=0,  pady=0, sticky='w')
symbol_2 = ttk.Combobox(mid_frame, values=symbol_of_event, width=5)
symbol_2.grid(row=2, column=1, padx=0,  pady=0, sticky='e')

def flag_depth_2_type():
    if depth_type_2var.get() == 1:
        Depth_entry_2_2.configure(state=ACTIVE) 
    else:
        Depth_entry_2_2.configure(state=DISABLED) 
    return  

depth_type_2var = IntVar(value=0)
Checkbutton(mid_frame, text="Interval", bg=bg1, background=bg3, command=flag_depth_2_type, variable=depth_type_2var, activebackground=bg3, font=font2).grid(row=2, column=2)
Label(mid_frame, text='Depth, m', font=font1, bg=bg3).grid(row=2, column=3)
Depth_entry_2_1 = ttk.Entry(mid_frame, width=5) 
Depth_entry_2_1.grid(row=2, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text=' - ', bg=bg3).grid(row=2, column=5)
Depth_entry_2_2 = ttk.Entry(mid_frame, width=5, state=DISABLED) 
Depth_entry_2_2.grid(row=2, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text='Short Description: ', font=font1, bg=bg3).grid(row=2, column=7)
short_description_2 = ttk.Entry(mid_frame, width=35) 
short_description_2.grid(row=2, column=8, padx=1, pady=5, sticky='w')

#Третья точка-интервал
Label(mid_frame, text='3. ', font=font1, bg=bg3).grid(row=3, column=0, padx=0,  pady=0, sticky='w')
symbol_3 = ttk.Combobox(mid_frame, values=symbol_of_event, width=5)
symbol_3.grid(row=3, column=1, padx=0,  pady=0, sticky='e')

def flag_depth_3_type():
    if depth_type_3var.get() == 1:
        Depth_entry_3_2.configure(state=ACTIVE) 
    else:
        Depth_entry_3_2.configure(state=DISABLED) 
    return  

depth_type_3var = IntVar(value=0)
Checkbutton(mid_frame, text="Interval", bg=bg1, background=bg3, command=flag_depth_3_type, variable=depth_type_3var, activebackground=bg3, font=font2).grid(row=3, column=2)
Label(mid_frame, text='Depth, m', font=font1, bg=bg3).grid(row=3, column=3)
Depth_entry_3_1 = ttk.Entry(mid_frame, width=5) 
Depth_entry_3_1.grid(row=3, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text=' - ', bg=bg3).grid(row=3, column=5)
Depth_entry_3_2 = ttk.Entry(mid_frame, width=5, state=DISABLED) 
Depth_entry_3_2.grid(row=3, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text='Short Description: ', font=font1, bg=bg3).grid(row=3, column=7)
short_description_3 = ttk.Entry(mid_frame, width=35) 
short_description_3.grid(row=3, column=8, padx=1, pady=5, sticky='w')

#Четвертая точка-интервал
Label(mid_frame, text='4. ', font=font1, bg=bg3).grid(row=4, column=0, padx=0,  pady=0, sticky='w')
symbol_4 = ttk.Combobox(mid_frame, values=symbol_of_event, width=5)
symbol_4.grid(row=4, column=1, padx=0,  pady=0, sticky='e')

def flag_depth_4_type():
    if depth_type_4var.get() == 1:
        Depth_entry_4_2.configure(state=ACTIVE) 
    else:
        Depth_entry_4_2.configure(state=DISABLED) 
    return  

depth_type_4var = IntVar(value=0)
Checkbutton(mid_frame, text="Interval", bg=bg1, background=bg3, command=flag_depth_4_type, variable=depth_type_4var, activebackground=bg3, font=font2).grid(row=4, column=2)
Label(mid_frame, text='Depth, m', font=font1, bg=bg3).grid(row=4, column=3)
Depth_entry_4_1 = ttk.Entry(mid_frame, width=5) 
Depth_entry_4_1.grid(row=4, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text=' - ', bg=bg3).grid(row=4, column=5)
Depth_entry_4_2 = ttk.Entry(mid_frame, width=5, state=DISABLED) 
Depth_entry_4_2.grid(row=4, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text='Short Description: ', font=font1, bg=bg3).grid(row=4, column=7)
short_description_4 = ttk.Entry(mid_frame, width=35) 
short_description_4.grid(row=4, column=8, padx=1, pady=5, sticky='w')

#Пятая точка-интервал
Label(mid_frame, text='5. ', font=font1, bg=bg3).grid(row=5, column=0, padx=0,  pady=0, sticky='w')
symbol_5 = ttk.Combobox(mid_frame, values=symbol_of_event, width=5)
symbol_5.grid(row=5, column=1, padx=0,  pady=0, sticky='e')

def flag_depth_5_type():
    if depth_type_5var.get() == 1:
        Depth_entry_5_2.configure(state=ACTIVE) 
    else:
        Depth_entry_5_2.configure(state=DISABLED) 
    return  

depth_type_5var = IntVar(value=0)
Checkbutton(mid_frame, text="Interval", bg=bg1, background=bg3, command=flag_depth_5_type, variable=depth_type_5var, activebackground=bg3, font=font2).grid(row=5, column=2)
Label(mid_frame, text='Depth, m', font=font1, bg=bg3).grid(row=5, column=3)
Depth_entry_5_1 = ttk.Entry(mid_frame, width=5) 
Depth_entry_5_1.grid(row=5, column=4, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text=' - ', bg=bg3).grid(row=5, column=5)
Depth_entry_5_2 = ttk.Entry(mid_frame, width=5, state=DISABLED) 
Depth_entry_5_2.grid(row=5, column=6, padx=5, pady=5, sticky='w'+'e'+'n'+'s')
Label(mid_frame, text='Short Description: ', font=font1, bg=bg3).grid(row=5, column=7)
short_description_5 = ttk.Entry(mid_frame, width=35) 
short_description_5.grid(row=5, column=8, padx=1, pady=5, sticky='w')
#---------------------------------------------------------------------------------------------
# Depth_entry_1_1.insert(0, "1800")
# variable=type_well, 
#описание процесса и кнопка запуска
st = ScrolledText(down_frame, width=85,  height=10, bd=1.5, font = 'Arial 10')
st.grid(row=1, column=1, padx=5, pady=0, sticky='w'+'e'+'n'+'s')
Button(down_frame, text="Start Processing", command=trajectory_build_function, width=85).grid(row=0, column=1, padx=5, pady=3, sticky='w'+'e'+'n'+'s')

#Меню
menu_bar = Menu(window_main)

def calculator():
    os.system("C:/WINDOWS/System32/calc.exe")
    return

def show_about():
    messagebox.showinfo(title="About", message="Version: 1.0\nAuthor: Stanislav Nikulin\nTelegram: @stan_nikulin\nDate: 2023\nLicense: MIT")
    

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=window_main.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Calculator", command=calculator)

menu_bar.add_cascade(label="Options", menu=edit_menu)

help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About...", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

window_main.config(menu=menu_bar)



window_main.mainloop()