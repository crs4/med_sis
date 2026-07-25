#######################
# Hydro PTF4MED
# ####################### 

to update the model 

1) go inside the django running container (the SIS should be up)

> docker compose exec -it django bash

2) modify the row 35 of the file: HYDROPTF4MED.py with the path of the new training set:

> cd /usr/src/s4m_catalogue/hydro_ptf
> vi HYDROPTF4MED.py
 
row 35:  file_path = "/usr/src/s4m_catalogue/hydro_ptf/HYDRO_GRAV_oct25.xlsx"

change HYDRO_GRAV_oct25.xlsx with the name of the xlsx file containing the new training set

3) then execute  

> rm -r *.pkl
> python HYDROPTF4MED.py


