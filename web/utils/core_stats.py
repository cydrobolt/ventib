# Ventrib Core Statistic Generator
import time
import random

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
        hour_of_day = time.gmtime(unix_ts).tm_hour + self.hour_offset

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

    def general_stats_total_sentences(self):
        l = len(list(filter(lambda k: k.time > (time.time() - 86400), self.data_array)))
        if l < 20:
            return "This user doesn't say much, with only %d sentences in the last 24 hours." % l
        return "This user said %d sentences in the last 24 hours." % l

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
        returnTRs = ""
        for i in data[:6]:
            returnTRs += """
          <tr>
            <td>{}</td>
            <td>{}</td>
          </tr>
          """.format(i[1], i[0])

        returnData = """
         <table class="small" style="font-size:80%">
            <thead>
              <tr>
                  <th data-field="word">Word</th>
                  <th data-field="occurences">Occurences</th>
              </tr>
            </thead>

            <tbody>
              {}
            </tbody>
         </table>
        """.format(returnTRs)
        # return "This user's most common words are %s." % ", ".join([i[1] for i in data[:20]])
        return returnData

    def most_common_time(self):
        d = {}
        for i in self.data_array:
            t = self.time_of_day(i.time)
            if t not in d:
                d[t] = 0
            d[t] += 1
        data = [(i[1], i[0]) for i in d.items()]
        return "This user tends to talk a lot during the %s." % max(data)[1]
