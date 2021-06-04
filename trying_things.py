import os
import pandas as pd

#note: this script assumes that first row is an index row
#if there is no index row, it will require some changes
#remove index_col from read_excel or set it to "none" 
#why are the column names in {}? if you want to use anything but "l c r" it can be helpful

path = r"C:\Users\kunge\Downloads\book1.xlsx"
table = pd.read_excel(path,index_col = 0) #file path of the table
save_path = os.path.join(os.path.dirname(path), os.path.basename(path)[:-5] + ".tex") #builds the file path were the table will be saved

def to_latex(table, save_path):
    table = table.round(2) #round all values to two decimal places
    table = table.fillna("x") #replace NaN with "x"
    tex_table = r"\begin{tabular}{l "
    for i in range(table.shape[1]):
        tex_table = tex_table + "r "
    if table.index.name:
        tex_table = tex_table + r"""}
\toprule
{"""   +  table.index.name + "}"
    else:
        tex_table = tex_table + r"""}
\toprule
"""
    for j in table.columns:
        tex_table = tex_table + "&{" + str(j) + "}\t"
    tex_table = tex_table + r"""\\
\midrule
"""
    # if you define a dict with that has colum names and the assigned units you can uncomment the following:
    # for m in table.columns:
    #     tex_table = tex_table + r"&\si{" + si_unit[m] + "}"
    # tex_table = tex_table + r"""\\
        # \midrule
        # """
    if table.index.name: #check if there is an index so it will included
        for k in table.index:
            tex_table = tex_table + str(k).replace("_" , r"\_" )
            for l in table.columns:
                tex_table = tex_table + "\t&" + str(table.loc[k,l])
            tex_table = tex_table + "\n"
    else:
        for k in table.index:   #if there is no index, no need to include it
            for l in table.columns:
                tex_table = tex_table + "\t&" + str(table.loc[k,l])
            tex_table = tex_table + "\n"

    tex_table = tex_table + r"""\bottomrule
\end{tabular}"""
    file = open(save_path, "w")
    file.write(tex_table)
    file.close()

try: #try to do the manual implementation, if it fails, resort to standard implementation
    to_latex(table, save_path)
except:
    table.to_latex(save_path,index = False)
    
