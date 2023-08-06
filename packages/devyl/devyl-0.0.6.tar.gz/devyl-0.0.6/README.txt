This library used for evaluate machine learning and deep learning algorithm, still on progress and will be improved as long as there are opportunity to do it.

Binary classification algorithm target for current phase:
1. SVM
2. Logistic Regression
3. KNN
4. Decision Tree 
5. Random Forest
6. Neural Network

How to initialise this library:
1. Type 'from devyl import evaluate' to call the library
2. create the function:
ML -- variablename = evaluate.binary(algorithm, xtrain, xtest, ytrain, ytest)
DL -- variablename = evaluate.neuralnet(algorithm, xtrain, xtest, ytrain, ytest)
-- it need algorithm that already been fit with training dataset.
comparison score -- variablename = evaluate.compare(listname)
-- it need the list of the score summary of all algorithm
3. The binary and neuralnet function contains:
- plot_confusionmatrix() -- for visualise confusion matrix
- print_score(string) -- this function will calculate the accuracy score, log loss, precision, recall, f1, and roc_auc score
for training and testing dataset
- auc_plot() or auc_plot(history, epochs) for neural network 
-- this function will visualise learning curve from the model with training and testing phase comparison
- score_table -- to call score summary from the model it will return array of metrics score
4. The compare function contains:
- plot_accuracycomparison() -- visualise accuracy score comparison between training and testing
- plot_lossccomparison() -- visualise loss score comparison between training and testing
- plot_precisioncomparison() -- visualise precision score comparison between class 1 and 0
- plot_recallcomparison() -- visualise recall score comparison between class 1 and 0
- plot_ROCcomparison() -- visualise roc_auc score comparison between training and testing



Please send an email to imthedevyl@gmail.com for any feedback to improve this library