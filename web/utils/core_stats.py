# Ventrib Core Statistic Generator
import time

foul_words = list(map(str.strip, open("badwords.txt").read().splitlines()))

class CoreStats:
    """ Generate stastics from an array of sentences

    List `data_array`:
        Indices:
            dictionary `[indice]`:
                String speech: Parsed Speech
                String date: UNIX timestamp
                String location: Longitude/Latitude
    """
    def __init__(self, data_array, hour_offset):
        self.data_array = data_array
        self.hour_offset = hour_offset

    def time_of_day(self, unix_ts):
        hour_of_day = time.localtime(unix_ts).tm_hour + self.hour_offset

        if hour_of_day < 5 or hour_of_day > 22:
            time_of_day = "night"
        elif hour_of_day < 22 and hour_of_day > 17:
            time_of_day = "evening"
        elif hour_of_day < 10 and hour_of_day > 5:
            time_of_day = "morning"
        else:
            time_of_day = "day"
        return time_of_day

    def foul_words_stats(self):
        foul_words_tod = {"morning": 0, "day": 0, "evening": 0, "night": 0}
        foul_words_num = 0

        for speech_fragment in self.data_array:
            speech = speech_fragment.text
            speech_location = speech_fragment.location
            speech_date = speech_fragment.time

            for fw in foul_words:
                if fw in speech:
                    foul_words_num += speech.count(fw)
            foul_words_tod[self.time_of_day(speech_date)] += 1

        maxfoul = max(foul_words_tod.values())
        if maxfoul > 2:
            foul_tod = list(filter(lambda k: k[1] == maxfoul, foul_words_tod.items()))[0][0]
            factoid = "This user seems to use the most foul language in the {}, with {} sentences containing foul language".format(foul_tod, maxfoul)
        else:
            factoid = "Hmm. This user doesn't seem to use much foul language, with only {} instances during the past day.".format(foul_words_num)

        return factoid
