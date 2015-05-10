
import pandas as pd
import datetime
from collections import Counter
from scipy.signal import argrelmax


def data_loader(filename):

	df = pd.read_csv(filename)
	df['date'] = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S'))

	return df

def wrangling(data_frame):

	c = Counter(data_frame['game'])
	top_games = []

	tmp_entries = set([])
	for item in c.items():
		tmp_entries.add(item[1])
	max_entries = max(tmp_entries)
	del(tmp_entries)

	for item in c.items():
		if item[1] == max_entries:
			top_games.append(item[0])

	# new CSV
	for game in top_games:
		df_1 = df[df['game'] == game].loc[:, ['date', 'game', 'current_players']]
		df_1['current_players'] = df_1['current_players'].apply(lambda x: x/df_1['current_players'].mean())
		top_time = get_avg_local_maxima(df_1)
		print "{} top players at {}h".format(game, top_time)
		# with open('data/test.csv', 'a') as f:
		# 	df_1.to_csv(f, header=False)


def get_avg_local_maxima(df):

	list_of_dates = df['date'].values.tolist()
	list_of_players = df['current_players'].values.tolist()
	days = set([])
	for date in list_of_dates:
		day = date.split(' ')[0]
		days.add(day)

	top_times = []
	for day in days:
		d = []
		p = []
		for count, date in enumerate(list_of_dates):
			if day in date:
				p.append(list_of_players[count])
				d.append(date)
		top_times.append(d[p.index(max(p))].split(' ')[1][:2])
	average_top_time = max(set(top_times), key=top_times.count)

	return average_top_time


if __name__ == '__main__':
	df = data_loader('data/steam_stats.csv')
	wrangling(df)