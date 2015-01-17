# Ventrib Core Statistic Generator
import time
import random
import json

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

    @staticmethod
    def time_of_day(unix_ts, offset):
        hour_of_day = time.gmtime(unix_ts).tm_hour + offset

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
                    foul_words_tod[self.time_of_day(speech_date, self.hour_offset)] += 1

        maxfoul = max(foul_words_tod.values())
        if maxfoul > 2:
            foul_tod = list(filter(lambda k: k[1] == maxfoul, foul_words_tod.items()))[0][0]
            factoid = "This user seems to use the most foul language in the {}, with {} sentences containing foul language".format(foul_tod, maxfoul)
        else:
            factoid = "Hmm. This user doesn't seem to use much foul language, with only {} instances during the past day.".format(foul_words_num)
        return factoid

    def general_stats_total_sentences(self):
        l = len(list(filter(lambda k: k.time > (time.time() - 86400), self.data_array)))
        if l < 20:
            return "This user doesn't say much, with only %d sentences in the last 24 hours." % l
        return "This user said %d sentences in the last 24 hours." % l

    def random_quote(self):
        tr_quote = random.choice(list(filter(lambda k: k.time > (time.time() - 86400), self.data_array)))
        return tr_quote.text

    def most_talk_area(self):
        today_words = list(filter(lambda k: k.time > (time.time() - 86400), self.data_array))

    def most_quiet_time(self):
        today_words = list(filter(lambda k: k.time > (time.time() - 86400), self.data_array))
        # quiet_tod = {"morning": 0, "day": 0, "evening": 0, "night": 0}
        quiet_tod = dict()
        for word in self.data_array:
            hour_of_day = time.gmtime(word.time).tm_hour + 5
            # quiet_tod[self.time_of_day(word.time, self.hour_offset)] += 1
            try:
                quiet_tod[hour_of_day] += 1
            except:
                quiet_tod[hour_of_day] = 1

        min_quiet_tod = min(quiet_tod)
        factoid = "This user seems to be the quietest during {}:00 to {}:00".format(min_quiet_tod, min_quiet_tod+1)
        return factoid

    def markov_chains(self):
        data = {}
        for i in list(filter(lambda k: k.time > (time.time() - 86400), self.data_array)):
            s = i.text.split()
            for idx, j in enumerate(s):
                if idx == len(s) - 1:
                    break
                if j not in data:
                    data[j] = []
                data[j].append(s[idx + 1])
        print(data)
        start = random.choice(list(data.keys()))
        sentence = [start]
        while len(sentence) < 40:
            if start not in data:
                break
            start = random.choice(data[start])
            sentence.append(start)
        return " ".join(sentence)

    def most_common_word(self):
        words = sum([i.text.split() for i in list(filter(lambda k: k.time > (time.time() - 86400), self.data_array))], [])
        d = {}
        for word in words:
            if word not in d:
                d[word] = 0
            d[word] += 1
        data = [(i[1], i[0]) for i in d.items()]
        data = sorted(data, reverse=True)
        # return "This user's most common words are %s." % ", ".join([i[1] for i in data[:20]])
        return data

    def least_common_word(self):
        words = sum([i.text.split() for i in list(filter(lambda k: k.time > (time.time() - 86400), self.data_array))], [])
        d = {}
        for word in words:
            if word.isnumeric():
                continue
            if word not in d:
                d[word] = 0
            d[word] += 1
        data = [(i[1], i[0]) for i in d.items()]
        data = sorted(data, reverse=False)
        # return "This user's most common words are %s." % ", ".join([i[1] for i in data[:20]])
        return data

    def most_common_time(self):
        d = {}
        for i in self.data_array:
            t = self.time_of_day(i.time, self.hour_offset)
            if t not in d:
                d[t] = 0
            d[t] += 1
        data = [(i[1], i[0]) for i in d.items()]
        return "This user tends to talk a lot during the %s." % max(data)[1]

class GraphStats:
    def __init__(self, science, illuminati):
        self.science = science
        self.illuminati = illuminati

    def times(self):
        data = [0 for i in range(12)]
        for k in self.science:
            data[((time.gmtime(k.time).tm_hour + self.illuminati) % 24) // 2] += 1

        return json.dumps({
                "labels": [str(i * 2) for i in range(12)],
                "datasets": [{
                    "label": "Ayy lmao 420 blaze it smoke pebbles daily",
                    "fillColor": "rgba(220, 220, 220, 0.5)",
                    "strokeColor": "rgba(220, 220, 220, 0.8)",
                    "highlightFill": "rgba(220, 220, 220, 0.75)",
                    "highlightStroke": "rgba(220, 220, 220, 0.1)",
                    "data": data
                }]
        })
