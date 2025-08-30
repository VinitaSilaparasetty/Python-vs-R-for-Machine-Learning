#import libraries
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

#create wifgets
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(642, 513)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(printhere)
        self.pushButton.setGeometry(QtCore.QRect(170, 180, 101, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 85, 131, 21))
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(6, 130, 151, 31))
        self.label2.setObjectName("label_2")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 290, 271, 192))
        self.listView.setObjectName("listView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def retranslateUi(self, MainWindow):
        translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(translate("MainWindow", "Twitter Sentiment Analysis"))
        self.pushButton.setText(translate("MainWindow", "ANALYZE"))
        self.label.setText(translate("MainWindow", "Enter Desired Hashtag: "))
        self.label2.setText(translate("MainWindow", "Number of Tweets to Analyze :"))
    def numberofSearchTerms(self):
        self.numberofSearchTerms = QtWidgets.QTextEdit(self.centralwidget)
        self.numberofSearchTerms.setGeometry(QtCore.QRect(170, 130, 104, 31))
        self.numberofSearchTerms.setObjectName("numberofSearchTerms")
    def searchTerm(self):
        self.searchTerm = QtWidgets.QTextEdit(self.centralwidget)
        self.searchTerm.setGeometry(QtCore.QRect(170, 80, 104, 31))
        self.searchTerm.setObjectName("searchTerm")
    
    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

                
   
  
#import secret keys for tweepy   
con_key="***"
con_sec="***"
acc_tok="***"
acc_sec="***"


auth=tweepy.OAuthHandler(consumer_key=con_key,consumer_secret=con_sec)
auth.set_access_token(acc_tok,acc_sec)
api=tweepy.API(auth)

search_term=input("Enter Desired Hashtag: ")
num_search=int(input("Number of Tweets to Analyze :"))

tweets=tweepy.Cursor(api.search, q=search_term, lang="English").items(num_search)

#initialize counters to 0
pos=0.00
neg=0.00
mix=0.00
pol=0.00

#sentiment analysis
for tweet in tweets:
    print(tweet.text)
    analysis=TextBlob(tweet.text)
    pol+=analysis.sentiment.pol
    if(analysis.sentiment.pol==0.00):
        mix+=1
    elif(analysis.sentiment.pol<0.00):
        neg+=1
    elif(analysis.sentiment.pol>0.00):
        pos+=1

positive=percentage(pos,num_search)
negative=percentage(neg,num_search)
mixed=percentage(mix,num_search)
polarity=percentage(pol,num_search)

positive=format(positive,'.2f')
negative=format(negative,'.2f')
mixed=format(mixed,'.2f')

print('People's Reactions to'+searchTerm)

#categorize reactions

if(polarity==0):
    print("Mixed Views")
elif(polarity<0.00):
    print("Negatively")
elif(polarity>0.00):
    print("Positively")

labels=["Positive["+str(positive)+"%]","Mixed Views["+str(mixed)+"%]","Negative["+str(negative)+"%]"]
sizes=[positive,mixed,negative]
colors=["orange","magenta","red"]
patches,texts=plt.pie(sizes,colors=colors,startangle=90)
plt.legend(patches,labels,loc="best")
plt.title("People's Reactions to"+searchTerm)
plt.axis("equal")
plt.tight_layout()
plt.show()
