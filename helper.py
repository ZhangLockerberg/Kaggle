import pandas as pd

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