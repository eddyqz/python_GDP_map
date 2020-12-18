# python_GDP_map
This repo contains a program to read GDP data and render to an SVG map, a GDP data table (CSV file), and the rendered maps.

To run this program, you need a GDP data table in the form of a CSV file. 
Use the test_render_world_map() function to run the program. 
The test_render_world_map() contains a gdpinfo dictionary, which is a dictionary that contains some key information regarding the data table.
Change the information within the gdpinfo dictionary to fit the particular data table that you are working with.

When test_render_world_map() is called, the program will read data from the CSV file, extract GDP data for all countries for a particular year,
then display the data in a world map. The varying levels of shading on the map represent different levels of GDP (darker for higher GDP).
Please note that the numbers on the rendered maps do not represent actual GDP; these numbers are log base 10 of the actual GDP in order to reduce the contrast in 
shading on the map.
