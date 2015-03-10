#!/usr/bin/env python
# Description: Script to get game stats from Steam
__author__ = 'ignacioelola'

import csv
import time
import importio_rsc


class SaveData():

    def __init__(self):
        self.filename = None

    def initialize_files(self, file1):

        self.filename = file1

        # Write headers in the files (as well as blank them if they exist)
        # with open(self.filename, "w") as infile:
        #     writer = csv.writer(infile)
        #     writer.writerow(["timestamp", "current_players", "peak_today", "game", "game_url", "current_price", "price"])

    def save_result(self, results):

        timestamp = time.time()

        for result in results:
            game = result.get("game/_text").encode("utf-8")
            current_player = result.get("current_players")
            peak_today = result.get("peak_today")
            game_url = result.get("game")

            new_row = [timestamp, current_player, peak_today, game, game_url]

            with open(self.filename, "a") as infile:
                writer = csv.writer(infile)
                writer.writerow(new_row)


def main():
    guid = "f9c66c13-6aa7-4473-bbd7-46bc5d89a35f"

    source_url = "http://store.steampowered.com/stats/"

    output_filename = "data/steam_stats.csv"

    data_savior = SaveData()
    data_savior.initialize_files(output_filename)

    # Get stats
    query = {"input": {"webpage/url": source_url}}
    response = importio_rsc.query_api(query, guid)

    if "results" not in response:
        time.sleep(5)
        query = {"input": {"webpage/url": source_url}}
        response = importio_rsc.query_api(query, guid)

    if "results" in response:
        data_savior.save_result(response["results"])


if __name__ == '__main__':

    main()
