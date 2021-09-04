if __name__ == '__main__':
    # main 파일을 엔트리포인트로 사용할 경우, path에 폴더 경로를 추가해 절대 경로로 임포트가 가능하게 함
    from sys import path
    import os
    path.append(os.path.dirname(__file__))

import json
import base64
import sandol_constant as Constant
import random

def lambda_handler(event, context):
    try:
        return_string = ''
        request_body = event['body']
        request_body = json.loads(base64.b64decode(request_body))

        param = request_body['action']['params']
        key = list(param.keys())
        func_name = key[0]
        key_values = list(param.values())
        ACCESS_ID = str(request_body['userRequest']['user']['id'])  # 접근 권한을 가진 ID 확인용

        module_function = Constant.KEY_SET[key[0]]  # 입력된 파라미터에 맞는 함수 지정
        input_params = Constant.PARAM_EXIST_FUNCTION[key[0]]

        if len(input_params) == 0:  # 파라미터가 없는 기능 함수의 경우 모두 여기서 처리 가능

            if func_name == 'perm_chk':
                from return_type_generator import return_type as GEN
                return_string = GEN().set_text(ACCESS_ID)

            else:
                return_string = module_function()

        elif len(input_params) == 1:    # 파라미터가 1개인 경우, but subway는 플러그인을 가지므로, 따로 처리
            if func_name == 'subway':
                time = str(json.loads(request_body['action']['detailParams']['date_time']['value'])['time'])
                return_string = module_function(time)

            elif func_name == 'read_meal':
                return_string = module_function(ACCESS_ID)
            else:
                return_string = module_function(key_values[0])

        else:
            if func_name == 'read_feedback':
                if(str(key_values[0]) != '2'):
                    return_string = module_function[0](ACCESS_ID)
                else:
                    return_string = module_function[1](ACCESS_ID)

            elif func_name == 'store_name':
                upload_date = json.loads(key_values[3])
                return_string = module_function(key_values[0], key_values[1], key_values[2], upload_date['date'],
                                                ACCESS_ID)

            elif func_name == 'reset_meal':
                date = str(json.loads(param[key[0]])['date'])
                return_string = module_function(ACCESS_ID, date)


    except Exception as e:
        return_string = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": f"산돌이 기능 업데이트중입니다! 일부 기능이 사용이 제한됩니다{e}"
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "messageText": "도움말",
                        "action": "message",
                        "label": "도움말"
                    }
                ]
            }
        }
    print(return_string)
    return {
        'statusCode': 200,
        'body': json.dumps(return_string),
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

# if __name__ == "__main__":
#     from test_constant import *
#     print(lambda_handler(JSON_DATA, "asdf"))