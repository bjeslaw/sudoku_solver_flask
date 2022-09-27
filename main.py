import logging
from sys import stderr
from flask import Flask, render_template, request, flash
# from sys import stderr
import pandas as pd 
import numpy as np

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = "secret_key_1755"
## secret key means nothing, needing to avoid some stupid error 

#######################################################################################################################################
def iter_solver(df, print_status = False): 

    df_possible = df.copy()
    
    break_flg = False

    iter_num = 0 

    while not break_flg: 

        df_possible_previous = df_possible.copy()

        #### check all possible values

        for i in df_possible.index: 
            for j in df_possible.columns: 
                if len(df_possible.loc[i,j]) == 1: 
                    drop_value = df_possible.loc[i,j][0]
        #             maybe here we need not len(x) > 1 but exactly check i,j only
                    df_possible.loc[i,:] = df_possible.loc[i,:].apply(lambda x: [y for y in x if y != drop_value] if len(x) > 1 else x)
                    df_possible.loc[:,j] = df_possible.loc[:,j].apply(lambda x: [y for y in x if y != drop_value] if len(x) > 1 else x)
                    for i_s in [x for x in df_possible.index.to_list() if x // 3 == i // 3]:
                        for j_s in [x for x in df_possible.index.to_list() if x // 3 == j // 3]:
                            if (i_s == i) and (j_s == j):
                                pass
                            else:
                                df_possible.loc[i_s,j_s] = [y for y in df_possible.loc[i_s,j_s] if y != drop_value]
                else: 
                    pass

        ###### check if some value is possible in only one place in a row / columns or square    

        for v in range(1,10): 

            #### check by rows 
            tmp = df_possible.applymap(lambda x: 1 * (v in x))

            tmp = tmp.loc[tmp.sum(axis = 1).where(lambda x: x == 1).dropna().index,:]\
                .mask(lambda x: x == 0)\
                .reset_index()\
                .rename(columns = {'index': 'k_i'})\
                .melt(id_vars = 'k_i', var_name = 'k_j', value_name = 'new_val')\
                .dropna()\
                .pipe(lambda _df: _df.assign(new_val = [[v]] * _df.shape[0]))

            for _, vals in tmp.iterrows():
                df_possible.loc[vals['k_i'], vals['k_j']] = vals['new_val']


            #### check by columns
            tmp = df_possible.applymap(lambda x: 1 * (v in x))

            tmp = tmp.loc[:,tmp.sum(axis = 0).where(lambda x: x == 1).dropna().index]\
                .mask(lambda x: x == 0)\
                .reset_index()\
                .rename(columns = {'index': 'k_i'})\
                .melt(id_vars = 'k_i', var_name = 'k_j', value_name = 'new_val')\
                .dropna()\
                .pipe(lambda _df: _df.assign(new_val = [[v]] * _df.shape[0]))

            for _, vals in tmp.iterrows():
                df_possible.loc[vals['k_i'], vals['k_j']] = vals['new_val']


            #### check by squares

            tmp = df_possible.applymap(lambda x: 1 * (v in x))

            tmp.index.name = 'k_i'
            tmp.columns.name = 'k_j'

            tmp = tmp\
                .reset_index()\
                .melt(id_vars = 'k_i', value_name = 'val')\
                .assign(index_group = lambda _df: _df['k_i'] // 3 * 3 + _df['k_j'] // 3)\
                .pipe(lambda _df: _df.merge(
                    _df.groupby('index_group')['val'].sum().reset_index()\
                    .rename(columns = {'val': 'total_val'})
                ))\
                .where(lambda x: x['total_val'] == 1)\
                .where(lambda x: x['val'] == 1)\
                .dropna()\
                .astype(int)\
                .drop(columns = ['index_group', 'total_val'])\
                .rename(columns = {'val': 'new_val'})\
                .pipe(lambda _df: _df.assign(new_val = [[v]] * _df.shape[0]))

            for _, vals in tmp.iterrows():
                df_possible.loc[vals['k_i'], vals['k_j']] = vals['new_val']

        break_flg = (df_possible == df_possible_previous).min().min()

        iter_num = iter_num + 1
        if print_status:
            print(iter_num)
        
    return df_possible

#######################################################################################################################################

@app.route("/")
# def index_empty():
#     return index()


@app.route("/hello")
def index():
    flash("Fill the numbers you know:")
    return render_template("index.html")

@app.route("/solve_sudoku", methods=["POST","GET"])

def solve():
    # flash("sum is {}".format(int(request.form['x1']) + int(request.form['x2'])))
    # print('antoshka', file = stderr)
    input_list = [request.form['x1'], request.form['x2'], request.form['x3'], request.form['x4'], request.form['x5'], request.form['x6'], request.form['x7'], request.form['x8'], request.form['x9'], 
                request.form['x10'], request.form['x11'], request.form['x12'], request.form['x13'], request.form['x14'], request.form['x15'], request.form['x16'], request.form['x17'], request.form['x18'], 
                request.form['x19'], request.form['x20'], request.form['x21'], request.form['x22'], request.form['x23'], request.form['x24'], request.form['x25'], request.form['x26'], request.form['x27'], 
                request.form['x28'], request.form['x29'], request.form['x30'], request.form['x31'], request.form['x32'], request.form['x33'], request.form['x34'], request.form['x35'], request.form['x36'], 
                request.form['x37'], request.form['x38'], request.form['x39'], request.form['x40'], request.form['x41'], request.form['x42'], request.form['x43'], request.form['x44'], request.form['x45'], 
                request.form['x46'], request.form['x47'], request.form['x48'], request.form['x49'], request.form['x50'], request.form['x51'], request.form['x52'], request.form['x53'], request.form['x54'], 
                request.form['x55'], request.form['x56'], request.form['x57'], request.form['x58'], request.form['x59'], request.form['x60'], request.form['x61'], request.form['x62'], request.form['x63'], 
                request.form['x64'], request.form['x65'], request.form['x66'], request.form['x67'], request.form['x68'], request.form['x69'], request.form['x70'], request.form['x71'], request.form['x72'], 
                request.form['x73'], request.form['x74'], request.form['x75'], request.form['x76'], request.form['x77'], request.form['x78'], request.form['x79'], request.form['x80'], request.form['x81']]
    

    # print(input_list, file = stderr)
    input_arr_check = [float(x) if x != '' else 1 for x in input_list]

    input_list = [int(float(x)) if x != '' else 0 for x in input_list]

    ## fixed good sudoku if empty input:
    if pd.Series(input_list).max() == 0:
        input_list = [4, 5, 2, 1, 3, 7, 6, 9, 8, 3, 9, 6, 5, 8, 2, 7, 1, 4, 8, 1, 7, 9,
                    4, 6, 5, 3, 2, 5, 7, 3, 6, 1, 4, 8, 2, 9, 9, 6, 4, 7, 2, 8, 3, 5,
                    1, 2, 8, 1, 3, 9, 5, 4, 7, 6, 1, 2, 5, 4, 6, 3, 9, 8, 7, 6, 3, 8,
                    2, 7, 9, 1, 4, 5, 7, 4, 9, 8, 5, 1, 2, 6, 3]

    #################################################################

    df = pd.DataFrame({'val':input_list}).reset_index()\
        .rename(columns = {'index':'index_group'})\
        .assign(row_n = lambda _df: _df.index_group // 9)\
        .assign(col_n = lambda _df: _df.index_group % 9)\
        .pivot(
            index = 'row_n', 
            columns = 'col_n',
            values = 'val'
        ).mask(lambda x: x == 0)

    df = pd.DataFrame(df.values)
    
    df_possible = df.fillna(0).astype(int)\
        .applymap(lambda x: [x] if x != 0 else [*range(1,10)])

    ## solving 

    alternatives = []
    solution_found = False
    

    print_status = False

    ## check for valid number input (only digits 1,2,3,4,5,6,7,9)
    valid_values_flg = min([(x in [*range(1,10)]) for x in input_arr_check])
    if not valid_values_flg: 
        solution_found = True


    ## quick check that there is no duplicates in one row/columns/square in input:
    no_solution_input = False

    tmp = df.copy()
    tmp.index.name = 'k_i'
    tmp.columns.name = 'k_j'
    tmp = tmp\
        .reset_index()\
        .melt(id_vars = 'k_i', value_name = 'val')\
        .assign(index_group = lambda _df: _df['k_i'] // 3 * 3 + _df['k_j'] // 3)

    bad_row = pd.Series([df.loc[i].value_counts().max() for i in df.index]).max() > 1
    bad_column = pd.Series([df.loc[:,j].value_counts().max() for j in df.columns]).max() > 1
    bad_square = tmp.groupby('index_group')['val'].value_counts().max() > 1

    del tmp 

    print('bad_row: {}\nbad_column: {}\nbadsquare: {}'.format(bad_row, bad_column, bad_square), file = stderr)
    print('rows: {}'.format([df.loc[i].value_counts().max() for i in df.index]))
    print('columns: {}'.format([df.loc[:,j].value_counts().max() for j in df.columns]))

    if max(bad_row,bad_column,bad_square):
        no_solution_input = True
        solution_found = True
    ####################################
    

    while not solution_found: 

        df_possible = iter_solver(df_possible)

        if df_possible.applymap(lambda x: len(x)).max().max() == 1:
            if df_possible.applymap(lambda x: len(x)).min().min() == 1:
            
                nunique_1 = df_possible.applymap(lambda x: x[0]).nunique().min()
                nunique_2 = df_possible.applymap(lambda x: x[0]).T.nunique().min()
                nunique_3 = df_possible\
                    .applymap(lambda x: x[0])\
                    .reset_index()\
                    .melt(id_vars = 'k_i')\
                    .assign(index_group = lambda _df: _df['k_i'] // 3 * 3 + _df['k_j'] // 3)\
                    .groupby('index_group')['value'].nunique().min()
                
                if min(nunique_1, nunique_2, nunique_3) < 9:
                    if print_status:
                        print('we made error! trying alternative')
                    try:
                        df_possible = alternatives.pop()
                    except:
                        # print('ERROR: no solution!')
                        break
                ## alternative was wrong, come back to previous fork             
                else: 
                    # flash('solution found!')
                    solution_found = True  
                ## найдено решение
            else: 
                if print_status:
                    print('we made error! trying alternative')
                try:
                    df_possible = alternatives.pop()
                except:
                    # print('ERROR: no solution!')
                    break
            ## alternative was wrong, come back to previous fork 
        else:  
            if print_status:
                print('no more logical moves, trying random step')
            ## no move logical moves, searching for optimal cell (with least possible variants) to try random alternatives
            min_length = df_possible.applymap(lambda x: len(x) if len(x) > 1 else np.nan).min().min()
            variants = df_possible.where(lambda _df: _df.applymap(lambda x: len(x)) == min_length).reset_index()\
                .melt(id_vars = 'k_i', value_name = 'possible_numbers').dropna()\
                .reset_index(drop = True).loc[0]

            for pos_num in variants['possible_numbers']:
                tmp = df_possible.copy()
                tmp.loc[variants['k_i'], variants['k_j']] = [pos_num]
                alternatives.append(tmp)

            try:
                df_possible = alternatives.pop()
            except:
                # print('ERROR: no solution!')
                break

    if valid_values_flg:
        if solution_found and not no_solution_input:
            flash("Solution found!")
            tmp = df_possible.applymap(lambda x: x[0])
            return render_template('solution.html',  tables=[
                tmp.style\
                .set_uuid('solution')\
                .hide_index()\
                .hide_columns()\
                .to_html()])
        else:
            flash("ERROR: no solution :(")
            return render_template('solution.html')           
    else: 
        flash("Error in data! Please enter numbers in range 1...9")
        return render_template('solution.html')
 