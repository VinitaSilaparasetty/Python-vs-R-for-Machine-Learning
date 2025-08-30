#import libraries
from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt


def percentage(part,whole):
    return 100*float(part)/float(whole)

#secret keys for tweepy
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
