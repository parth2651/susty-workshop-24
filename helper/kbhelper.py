import json
import time
import boto3

#retrive results from KB
def retrieve(bedrock_agent_client,query, KB_ID, numberOfResults=3):
    return bedrock_agent_client.retrieve(
        retrievalQuery= {
            'text': query
        },
        knowledgeBaseId=KB_ID,
        retrievalConfiguration= {
            'vectorSearchConfiguration': {
                'numberOfResults': numberOfResults,
                'overrideSearchType': "HYBRID", # optional
            }
            
        }
    )

#retrive results from KB and generate response
def retrieveandgenerate(bedrock_agent_client,prompt, KB_ID, model_arn):
    #region = 'us-west-2'
    #model_arn = "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    return bedrock_agent_client.retrieve_and_generate(
            input={
                'text': prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': model_arn,
                }
            }
        )

# fetch context from the response
def get_contexts(retrievalResults):
    contexts = []
    parsed_data = json.loads(json.dumps(retrievalResults))
    content_and_text = []
    for result in parsed_data['retrievalResults']:
        content = result['content']
        text = content['text']
        content_and_text.append({'content': content, 'text': text})
        for item in content_and_text:
            # print("Content:")
            # print(item['content'])
            # print("Text:")
            # print(item['text'])
            # print("---")
            contexts.append(item['text'])
    return contexts
