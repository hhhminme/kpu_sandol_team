# return_type_generator.py

## OverView

* 카카오 오픈빌더의 각 타입에 들어가는 인자 값을 함수의 파라미터로 받아 자동으로 리턴 값을 생성해주는  Python 코드
* 총 6종류의 JSON 형식을 지원함
  * Simple Text : 간단한 텍스트 타입
  * Simple Image : 간단한 이미지 타입
  * Basic Card : 기본 카드형 타입
  * Commerce Card : 제품 소개등을 할 때 사용하는 카드형 타입
  * List Card : 표현하고자 하는 대상이 다수일 때 효과적으로 사용하는 카드형 타입
  * Carousel : 여러 장의 카드를 하나의 메시지에 일렬로 포함하는 타입



## Usage of Basic Type

### Simple Text

<img src="./return_type_img/Text Type.JPG" style="zoom:50%;" />



```Python
def is_Text(self, text):
```

**필수 파라미터**

> text\<string\> : 출력할 string을 입력으로 받음



**사용 예시**

```python
import return_type_generator as Generator
gen = Generator()
result = gen.is_Text("<날씨 스킬 파트 실행>")
```

<img src="./return_type_img/Simple Text Test.JPG" style="zoom:100%;" />





### Basic Card

<img src="./return_type_img/Basic Card Type.JPG" style="zoom:50%;" />



```python
def is_Card(self,thumb_img, Button(), is_title = None, is_description = None): 
```

<img src="./return_type_img/Basic Card Field.JPG" style="zoom:50%;" />


**필수 파라미터**

> thumb_img \<string\> : img의 주소를 `string` 형태로 전달



**선택 파라미터**

> Button() \<dict\> : button 을 생성하는 dictionary(JSON) 형태로 전달.
>
> is_title \<string\> : 카드의 제목을 문자열 형태로 전달
>
> is_description \<string\> : 카드에 대한 설명을 문자열 형태로 전달



**사용 예시**

```python
import return_type_generator as Generator
gen = Generator()
result = gen.is_Card("https://raw.githubusercontent.com/hhhminme/kpu_sandol_team/main/img/logo1.png", is_title="logo", is_description = "<코로나 스킬 파트 실행>")
```

<img src="./return_type_img/Basic Card Test.JPG" style="zoom:100%;" />





### Commerce Card

```Python
def is_commerce(self,thumbnail, description, price, currency, Button(), is_discount = None, is_discountRate = None, is_discountedPrice = None, profile = None):
```

<img src="./return_type_img/Commerce Card Field.JPG" style="zoom:50%;" />

**필수 파라미터**

> description \<string\> : 판매 항목의 설명을 문자열 형태로 전달
>
> price \<int\> : 제품의 가격을 문자열 형태로 전달
>
> currency \<string\> : 제품 가격의 통화를 전달합니다 (`won`만 가능)
>
> thumbnail \<string\> : 썸네일 이미지 URL을 전달합니다.
>
> Button() : 기본적으로 `구매하기` 버튼이 생성되며, 추가 버튼을 전달합니다 (최대 2개)



**선택 파라미터**

> is_discount \<int\> : 제품의 할인한 금액을 전달합니다.
>
> is_discountRate \<int\> : 제품의 가격에 대한 할인된 가격의 비율을 전달합니다.
>
> is_discountPrice\<int\> : 제품의 가격에 대한 할인가(할인된 가격)을 전달합니다.
>
> profile : 제품을 판매하는 프로필 정보를 전달합니다.


### List Card
```Python
def is_List(self, title, data, is_Button = None): 
```
**필수 파라미터**

> title : 리스트 최 상단에 노출 될 제목  
> data :  리스트에 들어갈 값, [title, subtitle, link]의 형태를 가진 리스트가 들어가야함.  



**선택 파라미터**

> is_Button : 버튼 타입 파라미터가 들어가야함.




## Usage of Parameter Type

### Button

```python
def Button(self, **kwargs):
```

* **Kwargs** 에 들어갈 내용

  > `'label'` : 버튼에 들어가는 내용 <mark>(필수)</mark>
  >
  > `'action'` : 버튼 클릭시 수행되는 작업 <mark>(필수)</mark>
  >
  > `'webLinkUrl'`
  >
  > `'messageText'`
  >
  > `'phoneNumber'`
  >
  > `'blockId'`

  

* **action** 종류

  > - `webLink`: 웹 브라우저를 열고 webLinkUrl 의 주소로 이동합니다.
  > - `message`: 사용자의 발화로 messageText를 실행합니다. (바로가기 응답의 메세지 연결 기능과 동일)
  > - `phone`: phoneNumber에 있는 번호로 전화를 겁니다. `ex) 010-0000-1234`
  > - `block`: blockId를 갖는 블록을 호출합니다. (바로가기 응답의 블록 연결 기능과 동일)
  >   - messageText가 있다면, 해당 messageText가 사용자의 발화로 나가게 됩니다.
  >   - messageText가 없다면, button의 label이 사용자의 발화로 나가게 됩니다.
  >
  > - `share`: 말풍선을 다른 유저에게 공유합니다. share action은 특히 케로셀을 공유해야 하는 경우 유용합니다.



**사용 예시**

```python
try:
    a = gen.is_Card("https://avatars.githubusercontent.com/u/25563122?v=4", 
                            opt.Button(label="Test", action="webLink",
                            webLinkUrl="https://github.com/Cycrypto"),
                            is_description="Button Test2")
except Exception as e:
    a = gen.is_Card("https://avatars.githubusercontent.com/u/25563122?v=4", is_description=str(e))
            
return a
```



