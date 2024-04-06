import joblib  # Import joblib module
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import KFold
import numpy


class Classifier:
    def __init__(self, tossing_graph, developers, preprocessor):
        self.tossing_graph = tossing_graph
        self.developers = developers
        self.preprocessor = preprocessor

    def run(self):
        data = joblib.load('OutputFiles/data.pkl')

        df_new1, df_new2 = data[13344:], data[:13344]
        print("Training dataset :", len(df_new1))
        print("Testing Dataset :", len(df_new2))

        # Using pipeline and no bigram
        pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())])
        pipeline.fit(numpy.asarray(df_new1['text']), numpy.asarray(df_new1['class']))

        print("The accuracy for MultinomialNB is : ", end='')
        print(pipeline.score(numpy.asarray(df_new2['text']), numpy.asarray(df_new2['class'])))

        # cross validate using kfold =>folded into 10 samples
        pipeline = Pipeline([
            ('count_vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())])

        k_fold = KFold(n_splits=10, shuffle=True)
        scores = []
        for train_indices, test_indices in k_fold.split(data):
            train_text = numpy.asarray(data['text'][train_indices])
            train_y = numpy.asarray(data['class'][train_indices])

            test_text = numpy.asarray(data['text'][train_indices])
            test_y = numpy.asarray(data['class'][train_indices])

            pipeline.fit(train_text, train_y)
            score = pipeline.score(test_text, test_y)
            scores.append(score)
        avg_score = sum(scores) / len(scores)
        print("The accuracy for Kfold MultinomialNB Classifier is : ", end='')
        print(avg_score)

        # Give input here
        print("Enter bug description : ")
        examples = [self.preprocessor.stem_and_stop(input())]  # Use input() instead of raw_input()
        predictions = pipeline.predict(examples)
        print("The predicted developer is : " + self.developers[int(predictions[0])])
        self.tossing_graph.calculate_toss_possibility(self.developers[int(predictions[0])])


class TossingGraph:
    def __init__(self):
        self.graph = []
        self.developers = []

    def add_developer(self, developer):
        self.developers.append(developer)
        self.graph.append([])

    def calculate_toss_possibility(self, index):
        if index is not None:  # Check if index is not None
            print("Max possibility is for tossing from " + self.developers[index] + " -> " + \
                  self.developers[self.graph[index].index(max(self.graph[index]))])
        else:
            print("Error: Developer index is None.")


# Main function
def main():
    # Create instances of TossingGraph, developers, and Preprocessor
    tossing_graph = TossingGraph()
    developers = ["Developer 1", "Developer 2", "Developer 3"]  # Example list of developers
    preprocessor = Preprocessor()  # Assuming Preprocessor class is defined elsewhere

    # Create instance of Classifier
    clf = Classifier(tossing_graph, developers, preprocessor)

    # Run the classifier
    clf.run()


if __name__ == '__main__':
    main()
