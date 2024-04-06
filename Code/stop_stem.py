import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords


class Preprocessor:
    def __init__(self):
        try:
            self.stop_words = stopwords.words('english')
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = stopwords.words('english')
        self.stemmer = PorterStemmer()

    def stem_and_stop(self, line):
        result = []
        for word in line.split():
            if word not in self.stop_words:
                result.append("%s " % self.stemmer.stem(word))
        return ''.join(result)

    def process_file(self):
        try:
            with open('OutputFiles/formatted_input', 'r', encoding='utf-8') as input_file:
                lines = input_file.readlines()
        except UnicodeDecodeError as e:
            print(f"Error decoding file: {e}")
            return

        final_lines = []

        # TODO: Split the lines and perform the stemming and stop-word removal in multiple threads
        for line in lines:
            developer_split_index = line.rfind(" , ")
            final_lines.append(self.stem_and_stop(line[:developer_split_index]))
            final_lines.append("{0}".format(line[developer_split_index+1:]))

        try:
            with open('OutputFiles/stemmed_input', 'w', encoding='utf-8') as output_file:
                output_file.writelines(final_lines)
        except UnicodeEncodeError as e:
            print(f"Error encoding output file: {e}")
            return
