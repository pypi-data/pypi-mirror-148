import pandas as pd
from regbot import signal

#df = pd.read_csv('../../../jupyter/regbot_v4.csv')
#df = pd.read_csv('../../../crypto/freqtrade/sell.csv')
df = pd.read_csv('../../../jupyter/unbuy.csv')
#print(df.columns)


df = df[df['regbot-min'] == 1]
def getEnterSignal(open,close,lthr,sig):
    return signal(open,close,lthr, 'enter')
def getExitSignal(open,close,lthr,sig):
    return signal(open,close,lthr,'exit')


#print(df.columns)

#print(df.head())

df['enter_result'] = df.apply(lambda row: getEnterSignal(row['open'], row['close'], 0.3,'enter'), axis=1) # optimal 0.7126436781609196
df['exit_result'] = df.apply(lambda row: getExitSignal(row['open'], row['close'], 0.3,'exit'), axis=1)
#print(df.head())
#print(len(df[df['enter_result'] == 1]), len(df))
print(len(df[df['exit_result'] == 1]), len(df))


