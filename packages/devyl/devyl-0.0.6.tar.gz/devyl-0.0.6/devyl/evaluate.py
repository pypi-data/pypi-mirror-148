import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, auc
from sklearn.metrics import log_loss, confusion_matrix, roc_auc_score, roc_curve
import pandas as pd
from sqlalchemy import null
import tensorflow as tf
import seaborn as sns
import numpy as np

class binary(object):
    def __init__(self, algo, xtrain, xtest, ytrain, ytest ):
        self.xtest = xtest
        self.ytest = ytest
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.algo = algo
        self.roctest = null
   
    def display(self):
        sns.heatmap(self.cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('Prediction')
        plt.ylabel('Actual')

    #plot the confusion matrix
    def plot_confusionmatrix(self): #it need the model variable after fitting the data
        #prediction from testing dataset
        test_predict = self.algo.predict(self.xtest)
        
        #plot confusion matrix
        cm = confusion_matrix(self.ytest, test_predict)

        self.test_predict = test_predict
        self.cm = cm
        self.display() 
    
    #roc auc calculation
    def auc_calc(self):
        #calculate roc_auc_score
        test_prob = self.algo.predict_proba(self.xtest)[::,1]
        train_prob = self.algo.predict_proba(self.xtrain)[::,1]
        roctest = roc_auc_score(self.ytest, test_prob)
        roctrain = roc_auc_score(self.ytrain, train_prob)
        fpr_test, tpr_test, _ = roc_curve(self.ytest,  test_prob)
        fpr_train, tpr_train, _ = roc_curve(self.ytrain,  train_prob)

        self.roctest = roctest
        self.roctrain = roctrain
        self.fpr_test = fpr_test
        self.tpr_test = tpr_test
        self.fpr_train = fpr_train
        self.tpr_train = tpr_train
        self.test_prob = test_prob
        self.train_prob = train_prob

    # Roc Curve Characterics
    def auc_plot(self):
        if (self.roctest == null):
            self.auc_calc()

        plt.title("Area Under Curve")
        plt.plot(self.fpr_test, self.tpr_test, label="AUC Test="+str(self.roctest))
        plt.plot(self.fpr_train, self.tpr_train, label="AUC Train="+str(self.roctrain))
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.legend(loc=4)
        plt.grid(True)
        plt.show()

    def prints(self):           
        #print metrics score
        print("Confusion Matrix Accuracy Score = {:.2f}%\n".format(self.cmatrix))
        print("Accuracy Score: Training -> {:.2f}% Testing -> {:.2f}%\n".format(self.acctrain, self.acctest))
        print("Log Loss Training-> {} Testing -> {}\n".format(self.logtrain, self.logtest))
        print('Precision class 1: {:.2f}%\nPrecision class 0: {:.2f}%'.format(self.precision1, self.precision0))
        print('Recall class 1: {:.2f}%\nRecall class 0: {:.2f}%'.format(self.recall1, self.recall0))
        print('F1: {:.2f}%'.format(self.f1)) 
        print('ROC AUC Training-> {:.2f} Testing-> {:.2f}'.format(self.roctrain, self.roctest)) 

    #metrix function 
    def print_score(self, name): #algo = model, name = string of the model name
        predtrain = self.algo.predict(self.xtrain)
        
        #confussion matrix percentage
        tn, fp, fn, tp = self.cm.ravel()
        tst = self.ytest.count()
        cmatrix = ((tn + tp)/tst)*100    

        #accuracy score
        acctest = (accuracy_score(self.ytest, self.test_predict))*100
        acctrain = (accuracy_score(self.ytrain, predtrain))*100

        #log loss
        logtest = log_loss(self.ytest,self.test_predict)
        logtrain = log_loss(self.ytrain,predtrain)
                
        #classification report
        precision1 = (tp / (tp+fp))*100
        precision0 = (tn/(tn+fn))*100
        recall1 = (tp/(tp+fn))*100
        recall0 = (tn/(tn+fp))*100
        f1 = 2*(precision1 * recall1)/(precision1 + recall1)    
        overfit = acctrain - acctest

        if (self.roctest == null):
            self.auc_calc()

        score = [name, cmatrix, acctest, acctrain, overfit ,logtest, logtrain, precision1, precision0, recall1, recall0, f1,
        self.roctest, self.roctrain]

        self.cmatrix = cmatrix
        self.acctest = acctest
        self.acctrain = acctrain
        self.overfit = overfit
        self.logtest = logtest
        self.logtrain = logtrain
        self.precision1 = precision1
        self.precision0 = precision0
        self.recall1 = recall1
        self.recall0 = recall0
        self.f1 = f1
        self.score = score

        self.prints()
    
    #evaluation table
    def score_table(self):
        return self.score

class neuralnet:
    def __init__(self, algo, xtrain, xtest, ytrain, ytest ):
        #predict test
        test_predict = algo.predict(xtest)
        testeval = algo.evaluate(xtest, ytest)
        traineval = algo.evaluate(xtrain, ytrain)

        self.testeval = testeval
        self.traineval = traineval
        self.xtest = xtest
        self.ytest = ytest
        self.xtrain = xtrain
        self.ytrain = ytrain
        self.algo = algo
        self.test_predict = test_predict

    def plot_confusionmatrix(self):
        ypred = []
        for i in self.test_predict:
            if i>0.5:
                ypred.append(1)
            else:
                ypred.append(0)
        cm =tf.math.confusion_matrix(labels=self.ytest,predictions=ypred)
        self.cm = cm
        binary.display(self)


    def auc_plot(self, h, epoch):
        #plotting training and validation accuracy values
        epoch_range=range(1,epoch+1)
        plt.plot(epoch_range,h.history['accuracy'])
        plt.plot(epoch_range,h.history['val_accuracy'])
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train','Val'],loc='upper left')
        plt.show()

        #plotting training and validation loss values
        plt.plot(epoch_range,h.history['loss'])
        plt.plot(epoch_range,h.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train','Val'],loc='upper left')
        plt.show()
    
    def print_score(self, name): 
        tn, fp, fn, tp =tf.experimental.numpy.ravel(self.cm)
        tn = tn.numpy()
        fp = fp.numpy()
        fn = fn.numpy()
        tp = tp.numpy()
        cmatrix = ((tn + tp)/self.ytest.count())*100  

        acctest = (self.testeval[1])*100
        acctrain = (self.traineval[1])*100

        #log loss
        logtest = self.testeval[0]
        logtrain = self.traineval[0]
                
        #classification report
        precision1 = (tp / (tp+fp))*100
        precision0 = (tn/(tn+fn))*100
        recall1 = (tp/(tp+fn))*100
        recall0 = (tn/(tn+fp))*100
        f1 = 2*(precision1 * recall1)/(precision1 + recall1)

        #roc auc score
        roctest = self.testeval[2]
        roctrain = self.traineval[2]
        #insert the metrics score to list
        overfit = acctrain - acctest

        score = [name, cmatrix, acctest, acctrain, overfit ,logtest, logtrain, precision1, precision0, recall1, recall0, f1,
        roctest, roctrain]
        
        self.cmatrix = cmatrix
        self.acctest = acctest
        self.acctrain = acctrain
        self.overfit = overfit
        self.logtest = logtest
        self.logtrain = logtrain
        self.precision1 = precision1
        self.precision0 = precision0
        self.recall1 = recall1
        self.recall0 = recall0
        self.f1 = f1
        self.roctest = roctest
        self.roctrain = roctrain
        self.score = score

        #print metrics score
        binary.prints(self)

    def score_table(self):
        return self.score

class compare(object):
    def __init__(self, compare):
        self.compare = compare
    def generate(self):
        scr = pd.DataFrame(self.compare, columns = ['algo','c_matrix','acc_test','acc_train', 'overfit', 'loss_test', 'loss_train', 'prec1', 'prec0',
         'recall1','recall0','F1', 'roctest', 'roctrain'])
        self.scr = scr
        return scr
    
    def plot_sidebar(self, flag1, flag2, str1, str2):
        plt.figure(figsize=(10,20))
        ind = np.arange(len(self.scr['algo']))
        width = 0.4
        fig, ax = plt.subplots(figsize=(10,10))

        ax.barh(ind, flag1, width, color='#184e77', label=str1)
        ax.barh(ind + width, flag2, width, color='#03045e', label=str2)
        ax.set(yticks=ind + width, yticklabels=self.scr['algo'], ylim=[2*width - 1, len(self.scr['algo'])])
        plt.yticks(fontsize=20)
        plt.xticks(fontsize=20)
        ax.legend()
        plt.title(str1 + 'VS' + str2, fontsize=25)
        plt.show()


    def plot_accuracycomparison(self):
        self.plot_sidebar(self.scr['acc_test'], self.scr['acc_train'], 'Accuracy Test', 'Accuracy Train')
    
    def plot_losscomparison(self):
        self.plot_sidebar(self.scr['loss_test'], self.scr['loss_train'], 'Loss Test', 'Loss Train')
    
    def plot_precisioncomparison(self):
        self.plot_sidebar(self.scr['prec1'], self.scr['prec0'], 'Precision Class 1', 'Precision Class 0')
    
    def plot_recallcomparison(self):
        self.plot_sidebar(self.scr['recall1'], self.scr['recall0'], 'Recall Class 1', 'Recall Class 0')
    
    def plot_ROCcomparison(self):
        self.plot_sidebar(self.scr['roctest'], self.scr['roctrain'], 'Recall Class 1', 'Recall Class 0')
