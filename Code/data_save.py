import joblib
from pandas import DataFrame
import numpy


def save():
    with open('OutputFiles/stemmed_input', 'r', encoding='utf-8') as f:  # Open the file with the correct encoding
        pairs = []
        developers = set()

        for line in f:
            pair = line.rstrip().rsplit(' , ', 1)
            if len(pair) == 2:
                developers.add(pair[1])
                pairs.append((pair[0], pair[1]))

    developers_list = list(developers)
    pairs = [(text, developers_list.index(developer)) for (text, developer) in pairs]

    data = DataFrame(pairs, columns=['text', 'class'])

    # Shuffle the data
    data = data.reindex(numpy.random.permutation(data.index))

    # Save the data to a pickle file
    joblib.dump(data, 'OutputFiles/data.pkl', compress=9)

    return developers_list
