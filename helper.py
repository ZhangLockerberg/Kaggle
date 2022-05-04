import pandas as pd
import numpy as np

def preprocess_add_features(data, test):
    data['TotalSpended'] = data['RoomService'] + data['FoodCourt'] + data['ShoppingMall'] + data['Spa'] + data['VRDeck']
    test['TotalSpended'] = test['RoomService'] + test['FoodCourt'] + test['ShoppingMall'] + test['Spa'] + test['VRDeck']
    data[['id', 'num']] = data.PassengerId.str.split('_', -1, expand=True)
    explore = data.PassengerId.str.split('_', -1, expand=True)
    data_prep = pd.DataFrame()
    data_prep[['id','cum']] = explore.groupby(0).count().reset_index()
    data = pd.merge(data, data_prep, how='inner', on='id')
    data['Status'] = 'empty'
    data.loc[data.cum == 1, 'Status'] = 1
    data.loc[data.cum != 1, 'Status'] = 0
    # data.loc[data.cum == 2, 'Status'] = 'couple'
    # data.loc[data.cum == 3, 'Status'] = 'family'
    # data.loc[data.cum > 3, 'Status'] = 'tourist group'

    test[['id', 'num']] = test.PassengerId.str.split('_', -1, expand=True)
    test_explore = test.PassengerId.str.split('_', -1, expand=True)
    test_prep = pd.DataFrame()
    test_prep[['id','cum']] = test_explore.groupby(0).count().reset_index()
    test = pd.merge(test, test_prep, how='inner', on='id')
    test['Status'] = 'empty'
    test.loc[test.cum == 1, 'Status'] = 1
    test.loc[test.cum != 1, 'Status'] = 0
    # test.loc[test.cum == 2, 'Status'] = 'couple'
    # test.loc[test.cum == 3, 'Status'] = 'family'
    # test.loc[test.cum > 3, 'Status'] = 'tourist group'
    #spending status
    data['Consumption'] = 0
    data.loc[data.TotalSpended>0, 'Consumption'] = 1
    data.loc[data.TotalSpended<=0, 'Consumption'] = 0

    test['Consumption'] = 0
    test.loc[test.TotalSpended>0, 'Consumption'] = 1
    test.loc[test.TotalSpended<=0, 'Consumption'] = 0

    #split cabin into multiple columns
    data[['A','B','C']] = data.Cabin.str.split('/', -1, expand=True)
    test[['A','B','C']] = test.Cabin.str.split('/', -1, expand=True)
    return data, test

def make_t_change(data, test):
    t = data.append(test)
    t.reset_index(inplace=True)
    t.rename(columns={'index':'idx'}, inplace=True)
    empty = 0
    empty_index_list = []
    non_empty_index_list = []
    for i, _ in enumerate(t.Cabin):
        if str(_) == 'nan':
            empty += 1
            empty_index_list.append(i)
        else:
            non_empty_index_list.append(i)
    t['Deck'] = t.loc[non_empty_index_list,:].Cabin.apply(lambda x: str(x).split('/')[0])
    t['CabinNumber'] = t.loc[non_empty_index_list,:].Cabin.apply(lambda x: str(x).split('/')[1])
    t['CabinSide'] = t.loc[non_empty_index_list,:].Cabin.apply(lambda x: str(x).split('/')[2])
    t['id'] = t.PassengerId.apply(lambda x: str(x).split('_')[0])
    t['id_number'] = t.PassengerId.apply(lambda x: str(x).split('_')[1])
    t_change = t.sort_values(['id','id_number']).reset_index()
    return t_change

def findPrev(idx, t_change):
    t_change.CabinNumber = t_change.CabinNumber.astype('float')
    sub_t_slice = t_change[:idx]
    return dict(sub_t_slice.groupby(['Deck','CabinSide']).CabinNumber.max().astype('int'))

def findNext(idx, t_change):
    t_change.CabinNumber = t_change.CabinNumber.astype('float')
    sub_t_slice = t_change[idx:]
    return dict(sub_t_slice.groupby(['Deck','CabinSide']).CabinNumber.min().astype('int'))

def processAlgorithm(t_change):
    df_list = []
    idx_list = []
    for idx, t in enumerate(t_change.Cabin):
        if str(t) == 'nan':
            next_dic = findNext(idx, t_change)
            pointer = 0
            for key, val in findPrev(idx, t_change).items():
                pointer += 1
                d = str(key[0])
                v = val
                s = str(key[1])
                next_val = next_dic.get(key)
                if len(t_change.loc[t_change.id == t_change.loc[idx, 'id']]) > 1:
                    try:
                        arr = t_change.loc[(t_change.id == t_change.loc[idx, 'id']) & \
                                     (t_change.CabinNumber.astype('string') != 'nan'), 'Cabin'].unique()[0]
                        df_list.append([arr])
                        idx_list.append(idx)
                        break
                    except:
                        pass            
                if val == next_val:
                    df_list.append(['/'.join((d, v, s))])
                    idx_list.append(idx)
                    break
                if val+1 != next_val:
                    v = str(val+1)
                    try:
                        df_list.index(['/'.join((d, v, s))])
                        if str(t_change.CabinNumber[idx-1]) != 'nan':
                            df_list.append([t_change.Cabin[idx-1]])
                            idx_list.append(idx)
                        else:
                            df_list.append(df_list[-1])
                            idx_list.append(idx)
                    except:
                        df_list.append(['/'.join((d, v, s))])
                        idx_list.append(idx)
                    break
    df_array = np.array(df_list).reshape(-1).astype('object')
    idx_array = np.array(idx_list)
    return df_array, idx_array

def fit_generator(data, test):
    t_change = make_t_change(data, test)
    df_array, idx_array = processAlgorithm(t_change)
    
    for df, idx in zip(df_array, idx_array):
        t_change.loc[idx, 'Cabin'] = df

    train_idx, train_columns = list(range(data.shape[0])), list(data.columns)
    test_idx, test_columns = list(range(data.shape[0], t_change.shape[0])), list(test.columns)
    t_change.sort_values('index', inplace=True, ignore_index=True)
    t_change.reset_index(drop=True)
    train_data = t_change.loc[train_idx, train_columns]
    test_data = t_change.loc[test_idx, test_columns]
    return train_data, test_data