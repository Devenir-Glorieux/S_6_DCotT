# Drilling complication on the trajectory

Visualization is one of the most in-demand methods of presenting information in the modern world. It is an area that leverages one of the most powerful stacks of digital technologies. Therefore, I am pleased to present my script for visualizing a three-dimensional well trajectory with the ability to annotate depths and intervals of complications.

It all starts with selecting a data file. The script is capable of calculating True Vertical Depth (TVD) and other trajectory parameters. However, you need an Excel table with columns named 'MD' for Measure Depth, 'incl' for zenith angle, and 'azi' for azimuth. Please ensure that the columns are named exactly as specified, as the pandas library requires them to build the necessary dataframe.

After loading the trajectory, you can view the file path, the first and last 5 rows of the dataframe, and any other available information in the output field.

Upon clicking the 'Start Processing' button, a localhost window will open in your browser, displaying the trajectory visualization using the plotly library. If you want to mark specific points or intervals on the trajectory, you can enter the corresponding depth values. To indicate an interval, simply check the corresponding checkbox. By the way, you have 4 marker options for indicating depth along the wellbore (cross by default):

- 'circle'
- 'square'
- 'diamond'
- 'cross'

For intervals, specify depths in ascending order. You can also add a well name for display on the graph and provide a brief description of the complications (character limit is unlimited).

As an added bonus, the script offers various manipulations with the 3D projection of the well trajectory and includes built-in image export functionality.

![Drilling_copl_2](https://github.com/Devenir-Glorieux/S_6_DCotT/assets/95652620/8db1fb3f-b346-494d-af0f-5815f97f3884)


