{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fa19dd93",
   "metadata": {},
   "outputs": [],
   "source": [
    "def preprocess_add_features(data, test):\n",
    "    data['TotalSpended'] = data['RoomService'] + data['FoodCourt'] + data['ShoppingMall'] + data['Spa'] + data['VRDeck']\n",
    "    test['TotalSpended'] = test['RoomService'] + test['FoodCourt'] + test['ShoppingMall'] + test['Spa'] + test['VRDeck']\n",
    "    data[['id', 'num']] = data.PassengerId.str.split('_', -1, expand=True)\n",
    "    explore = data.PassengerId.str.split('_', -1, expand=True)\n",
    "    data_prep = pd.DataFrame()\n",
    "    data_prep[['id','cum']] = explore.groupby(0).count().reset_index()\n",
    "    data = pd.merge(data, data_prep, how='inner', on='id')\n",
    "    data['Status'] = 'empty'\n",
    "    data.loc[data.cum == 1, 'Status'] = 1\n",
    "    data.loc[data.cum != 1, 'Status'] = 0\n",
    "    # data.loc[data.cum == 2, 'Status'] = 'couple'\n",
    "    # data.loc[data.cum == 3, 'Status'] = 'family'\n",
    "    # data.loc[data.cum > 3, 'Status'] = 'tourist group'\n",
    "\n",
    "    test[['id', 'num']] = test.PassengerId.str.split('_', -1, expand=True)\n",
    "    test_explore = test.PassengerId.str.split('_', -1, expand=True)\n",
    "    test_prep = pd.DataFrame()\n",
    "    test_prep[['id','cum']] = test_explore.groupby(0).count().reset_index()\n",
    "    test = pd.merge(test, test_prep, how='inner', on='id')\n",
    "    test['Status'] = 'empty'\n",
    "    test.loc[test.cum == 1, 'Status'] = 1\n",
    "    test.loc[test.cum != 1, 'Status'] = 0\n",
    "    # test.loc[test.cum == 2, 'Status'] = 'couple'\n",
    "    # test.loc[test.cum == 3, 'Status'] = 'family'\n",
    "    # test.loc[test.cum > 3, 'Status'] = 'tourist group'\n",
    "    #spending status\n",
    "    data['Consumption'] = 0\n",
    "    data.loc[data.TotalSpended>0, 'Consumption'] = 1\n",
    "    data.loc[data.TotalSpended<=0, 'Consumption'] = 0\n",
    "\n",
    "    test['Consumption'] = 0\n",
    "    test.loc[test.TotalSpended>0, 'Consumption'] = 1\n",
    "    test.loc[test.TotalSpended<=0, 'Consumption'] = 0\n",
    "\n",
    "    #split cabin into multiple columns\n",
    "    data[['A','B','C']] = data.Cabin.str.split('/', -1, expand=True)\n",
    "    test[['A','B','C']] = test.Cabin.str.split('/', -1, expand=True)\n",
    "    return data, test"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
