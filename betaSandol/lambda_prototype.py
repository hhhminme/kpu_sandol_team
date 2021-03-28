import json
import lambda_prototype_module as Module


def lambda_handler(event, context):
    try:
        # request_body = json.loads(event['body'])
        # param = request_body['action']['params']
        # key = list(param.keys())  # 입력으로 들어오는 값을 여기서 처리함
        # # 여러개 들어오는 경우 필수 파라미터 명이 key[0]에 들어감
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(event)
                        }
                    }
                ]
            }
        }

    except Exception as e:
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": str(e)
                        }
                    }
                ]
            }
        }

    return {
        'statusCode': 200,
        'body': json.dumps(result),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }