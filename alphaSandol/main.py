if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os
    path.append(os.path.dirname(__file__))

import json
import base64
import sandol_constant as Constant

def lambda_handler(event, context):
    try:
        return_string = ''
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))
        param = request_body['action']['params']
        key = list(param.keys())
        func_name = key[0]
        key_values = list(param.values())
        ACCESS_ID = str(request_body['userRequest']['user']['properties']['botUserKey'])  # 접근 권한을 가진 ID 확인용

        module_function = Constant.KEY_SET[key[0]]  # 입력된 파라미터에 맞는 함수 ㅈ지정
        input_params = Constant.PARAM_EXIST_FUNCTION[key[0]]

        if len(input_params) == 0:
            return_string = module_function()

        elif len(input_params) == 1:
            return_string = module_function(key_values[0])

        else:
            if func_name == 'read_feedback':
                return_string = module_function(key_values[0], ACCESS_ID)

            elif func_name == 'store_name':
                upload_date = json.loads(key_values[3])
                return_string = module_function(key_values[0], key_values[1], key_values[2], upload_date['date'],
                                                ACCESS_ID)

            elif func_name == 'reset_meal':
                upload_date = json.loads(key_values[3])
                return_string = module_function(ACCESS_ID, upload_date)


    except Exception as e:
        return_string = {
                            "simpleText": {
                                "text": str(e)
                            }
                        }

    return {
        'statusCode': 200,
        'body': json.dumps(return_string),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }