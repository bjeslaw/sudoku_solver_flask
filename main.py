from flask import Flask, render_template, request, flash
import pandas as pd 
import numpy as np

app = Flask(__name__)
app.secret_key = "secret_key_1755"


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
        #             мб тут нужно не len(x) > 1, а именно те самые i,j обходить только
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

            #### по строкам
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


            #### по столбцам
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


            #### по квадратам

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
    flash("Fill the number you know:")
    return render_template("index.html")

@app.route("/solve_sudoku", methods=["POST","GET"])

def solve():
    # flash("sum is {}".format(int(request.form['x1']) + int(request.form['x2'])))
    input_list = [request.form['x1'], request.form['x2'], request.form['x3'], request.form['x4'], request.form['x5'], request.form['x6'], request.form['x7'], request.form['x8'], request.form['x9'], 
                request.form['x10'], request.form['x11'], request.form['x12'], request.form['x13'], request.form['x14'], request.form['x15'], request.form['x16'], request.form['x17'], request.form['x18'], 
                request.form['x19'], request.form['x20'], request.form['x21'], request.form['x22'], request.form['x23'], request.form['x24'], request.form['x25'], request.form['x26'], request.form['x27'], 
                request.form['x28'], request.form['x29'], request.form['x30'], request.form['x31'], request.form['x32'], request.form['x33'], request.form['x34'], request.form['x35'], request.form['x36'], 
                request.form['x37'], request.form['x38'], request.form['x39'], request.form['x40'], request.form['x41'], request.form['x42'], request.form['x43'], request.form['x44'], request.form['x45'], 
                request.form['x46'], request.form['x47'], request.form['x48'], request.form['x49'], request.form['x50'], request.form['x51'], request.form['x52'], request.form['x53'], request.form['x54'], 
                request.form['x55'], request.form['x56'], request.form['x57'], request.form['x58'], request.form['x59'], request.form['x60'], request.form['x61'], request.form['x62'], request.form['x63'], 
                request.form['x64'], request.form['x65'], request.form['x66'], request.form['x67'], request.form['x68'], request.form['x69'], request.form['x70'], request.form['x71'], request.form['x72'], 
                request.form['x73'], request.form['x74'], request.form['x75'], request.form['x76'], request.form['x77'], request.form['x78'], request.form['x79'], request.form['x80'], request.form['x81']]
    
    input_list = [int(x) if x != '' else 0 for x in input_list]

    # input_list = [0, 5, 0, 0, 3, 7, 6, 9, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0, 0,
    #    0, 0, 5, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
    #    1, 0, 8, 0, 0, 9, 5, 0, 7, 0, 1, 0, 0, 0, 6, 3, 0, 0, 7, 0, 3, 0,
    #    2, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 6, 0]


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


    # # ## fixit
    # solution_found = True


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
                    df_possible = alternatives.pop()   
                ## альтернатива оказалась неверна, переходим к предыдущей развилке                
                else: 
                    flash('solution found!')
                    solution_found = True  
                ## найдено решение
            else: 
                if print_status:
                    print('we made error! trying alternative')
                df_possible = alternatives.pop()   
            ## альтернатива оказалась неверна, переходим к предыдущей развилке
        else:  
            if print_status:
                print('no more logical moves, trying random step')
            ## программа застопорилась, появилась развилка, находим оптимальную ячейку для рандомного выбора
            min_length = df_possible.applymap(lambda x: len(x) if len(x) > 1 else np.nan).min().min()
            variants = df_possible.where(lambda _df: _df.applymap(lambda x: len(x)) == min_length).reset_index()\
                .melt(id_vars = 'k_i', value_name = 'possible_numbers').dropna()\
                .reset_index(drop = True).loc[0]

            for pos_num in variants['possible_numbers']:
                tmp = df_possible.copy()
                tmp.loc[variants['k_i'], variants['k_j']] = [pos_num]
                alternatives.append(tmp)

            df_possible = alternatives.pop()

    

    ############################

    # solution_list = [4, 5, 2, 1, 3, 7, 6, 9, 8, 3, 9, 6, 5, 8, 2, 7, 1, 4, 8, 1, 7, 9,
    #    4, 6, 5, 3, 2, 5, 7, 3, 6, 1, 4, 8, 2, 9, 9, 6, 4, 7, 2, 8, 3, 5,
    #    1, 2, 8, 1, 3, 9, 5, 4, 7, 6, 1, 2, 5, 4, 6, 3, 9, 8, 7, 6, 3, 8,
    #    2, 7, 9, 1, 4, 5, 7, 4, 9, 8, 5, 1, 2, 6, 3]
    # tmp = pd.DataFrame({'val':solution_list}).reset_index()\
    #     .rename(columns = {'index':'index_group'})\
    #     .assign(row_n = lambda _df: _df.index_group // 9)\
    #     .assign(col_n = lambda _df: _df.index_group % 9)\
    #     .pivot(
    #         index = 'row_n', 
    #         columns = 'col_n',
    #         values = 'val'
    #     )

    tmp = df_possible.applymap(lambda x: x[0])


    # return render_template("index.html")
    # return render_template("solution.html")

    return render_template('solution.html',  tables=[tmp.to_html(classes='output_numbers', header = False, index = False)])

 