from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_validate, cross_val_score, StratifiedKFold
from imblearn.pipeline import Pipeline as imbpipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import make_scorer, recall_score, precision_score, f1_score, precision_recall_fscore_support
import numpy as np
import warnings
#warnings.filterwarnings('ignore')  # "error", "ignore", "always", "default", "module" or "once"


def ml(company, df):
	vectorizer = TfidfVectorizer(min_df = 1,max_df = 0.5,ngram_range=(1,2))
	print(company)

	if company == 'sv':
		print('sv')
		Classifiers = [
		RandomForestClassifier(n_estimators=50, max_features=4,max_depth=1000, max_leaf_nodes=None, min_samples_split=100)] #,
		# LogisticRegression(C=100,solver='newton-cg', penalty='l2'),
		# SVC(kernel = 'poly', C=1, gamma=1),
		# DecisionTreeClassifier(criterion='entropy', max_depth=12),
		# MultinomialNB(alpha=0.01)]
	else:
		print('en')
		Classifiers = [
		RandomForestClassifier(n_estimators=500, max_features=1,max_depth=1000, max_leaf_nodes=None, min_samples_split=100)] #,
		# LogisticRegression(C=100,solver='newton-cg', penalty='l2'),
		# SVC(kernel = 'poly', C=1, gamma=1),
		# DecisionTreeClassifier(criterion='entropy', max_depth=12),
		# MultinomialNB(alpha=0.01)]
		
	print(df.at[0,'preprocessed_text'])
	for clf in Classifiers:
		pipeline = imbpipeline([('vectorizer', vectorizer), ('classifier', clf)])
		#pipeline = imbpipeline([('vectorizer', vectorizer), ('smote', SMOTE()), ('classifier', clf)])

		skf = StratifiedKFold(n_splits=5, shuffle=True)

		scoring = {'accuracy': 'accuracy',
			'recall -1': make_scorer(recall_score, labels = [-1]),
			'recall 0': make_scorer(recall_score, average='weighted', labels = [0]),
			'recall 1': make_scorer(recall_score, average='weighted', labels = [1]),
			'precision -1': make_scorer(precision_score, average='weighted', labels = [-1]),
			'precision 0': make_scorer(precision_score, average='weighted', labels = [0]),
			'precision 1': make_scorer(precision_score, average='weighted', labels = [1]),
			'f1-score -1': make_scorer(f1_score, average='weighted', labels = [-1]),
			'f1-score 0': make_scorer(f1_score, average='weighted', labels = [0]),
			'f1-score 1': make_scorer(f1_score, average='weighted', labels = [1])}

		score = cross_validate(pipeline, df['preprocessed_text'].astype('U'), df['tweet_polarity'], scoring=scoring, cv=skf)
		print('\n'+clf.__class__.__name__)
		scores_dict = __dict_help(score)
		print(scores_dict['test_accuracy'])


def __dict_help(scores_dict):
	scores_dict = {metric: round(np.mean(scores), 5) for metric, scores in scores_dict.items()}

	del scores_dict['fit_time']
	del scores_dict['score_time']

	for item in scores_dict:
		print(f'{item}: {scores_dict[item]}')
	return(scores_dict)
