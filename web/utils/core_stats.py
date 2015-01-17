# Ventrib Core Statistic Generator
import datetime
class CoreStats:
    """ Generate stastics from an array of sentences

    List `data_array`:
        Indices:
            dictionary `[indice]`:
                String speech: Parsed Speech
                String date: UNIX timestamp
                String location: Longitude/Latitude
    """
    def __init__(self, data_array, timezone):
        self.data_array = data_array
        self.timezone = timezone
    def time_of_day(self, unix_ts):
        hour_of_day = datetime.datetime.fromtimestamp(
            int(speech_date)
        ).strftime('%H')
        if hour_of_day > 5 or hour_of_day > 22:
            time_of_day = "night"
        elif hour_of_day < 22 and hour_of_day > 17:
            time_of_day = "evening"
        elif hour_of_day < 10 and hour_of_day > 5:
            time_of_day = "morning"
        else:
            time_of_day = "day"
        return time_of_day

    def foul_words_stats(self):
        foul_words = ["fuck", "dick", "ass", "bitch", "cunt", "shit"]
        foul_words_num = 0

        foul_words_tod["morning"] = 0
        foul_words_tod["day"] = 0
        foul_words_tod["evening"] = 0
        foul_words_tod["night"] = 0

        for speech_fragment in data_array:
            speech = speech_fragment["speech"]
            speech_location = speech_fragment["location"]
            speech_date = speech_fragment["date"]

            for fw in foul_words:
                if fw in speech:
                    foul_words_num += 1
            foul_words_tod[self.time_of_day(speech_date)] += 1
        maxfoul = max(foul_words_tod)
        if maxfoul > 2:
            foul_tod = foul_words_tod.index(maxfoul)
            factoid = "This user seems to use the most foul language in the {}, with {} sentences containing foul language".format(foul_tod, maxfoul)
        else:
            factoid = "Hmm. This user doesn't seem to use much foul language, with only {} instances during the past day.".format(foul_words_num)

        return foul_words_num
