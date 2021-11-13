from dapr.ext.grpc import App, BindingRequest
import json
from dapr.clients import DaprClient
from time import sleep
app = App()

@app.binding('tweetsBinding')
def binding(request: BindingRequest):
    tweet=json.loads(request.text())
    tweetText=tweet["text"]
    print(tweetText, flush=True)
    jsonqueue={ "message": tweet}
    
    
    # ,
    # "operation": "create"
    # }
    with DaprClient() as d:
        #resp = d.invoke_binding('signalrbinding', 'create', json.dumps(jsondata))
        resp = d.invoke_binding('tweetqueuebinding', 'create', json.dumps(jsonqueue))
        toto= resp.text()
        print(toto)


@app.binding('tweetqueuebinding')
def queuebinding(request: BindingRequest):
    tweet=json.loads(request.text())["message"]
    jsondata={
            'Target': 'newTweet',
            'Arguments': [
                {
                    'sender': 'dapr',
                    'text': 
                    {
                        'id':tweet["id"],
                        'text':tweet["text"],
                        'display': 'dim',
                        #image: "",
                        'date': tweet["created_at"],
                        'app': 'Gangogh',
                        'retweets': tweet["retweet_count"],
                        'quotedTweets': tweet["quote_count"],
                        'likes': tweet["favorite_count"],
                        'user': {
                            'nickname': tweet["user"]["screen_name"],
                            'name': tweet["user"]["name"],
                            'avatar': tweet["user"]["profile_image_url"],
                            'verified': tweet["user"]["verified"],
                            'locked': False
                            }
                    }
                }
            ]
        }
    with DaprClient() as d: 
        resp = d.invoke_binding('signalrbinding', 'create', json.dumps(jsondata))
        sleep(1)

    
    
app.run(50051)