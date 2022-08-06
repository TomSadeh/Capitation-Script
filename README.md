# Capitation Script



A script which downloads population data from stats.oecd,
and calculates standard population for all oecd countries and others with 3 different capitation formulae:
1. Standard Israel capitation formula.
2. Israel capitation formula with long-term care.
3. EU27 capitation formula with no long-term care.   
    
The capitation formulae can be adjusted in the added csv file named "cap.csv".
The date range can be change as desired here in the script.
YOU HAVE TO ENTER A PATH FOR THE CAPITATION FILE, else the script won't work.
Sources:
1. Israel standard capitation formula:

https://www.btl.gov.il/Mediniyut/Situation/haveruth1/2021/Documents/capitatia_122021.doc
        
It has 0-1 age group, so I averaged it with the 1-4 age-group, with a weighted average, where the weights are 1
and 3 respectively.

2. EU capitation and Israel capitation with long-term care formulae are from Ahdut, Politzer and Ben-Nun here:

https://tinyurl.com/5drzpuvm
        
Both docs are in the github repository as well.

If you have any questions please email dtsj89@gmail.com or tsadeh@kohelet.org.il.
