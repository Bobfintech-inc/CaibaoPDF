---
title: 接口说明
---
# 小京搜索

## 一、PDF转text(OCR通用文字识别)

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdf2text
```

#### 京智大脑

```bash
POST http://onlineapp.aip.bj.bob.test:8080/characterRecognition/pdf2x/api/v1/ocr/pdf2text

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE 527CC35B89ABC649FD169EF550B6D5AD |
```

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| outformat | txt/json  |  返回保文格式 调用不传就默认txt|
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |

#### Form Parameter

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | jpg/png/bmp/jpeg/pdf | 图片或者pdf文件（单张图片或者单页pdf） |

### 返回参数

#### 状态码

| status | message |
| ------ | ------- |
| create | 任务创建完成 |
| success | 任务结束，执行成功|
| running  | 任务执行中 |
| error  | 任务结束，执行失败 |
| waitting | 任务等待中 |
| full | 等待队列已满,系统繁忙,不能够添加新的任务|
| existed | 已存在 |

#### 同步请求示例

```python
filename = "tests/cases/pdf2txt/1.png"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2text"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "outformat": "json"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
```
```bash
$ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2text?taskId=test2&outformat=json' --form 'file=@./tests/cases/pdf2txt/1.png' 
```

```python
返回json格式
{
    "status": 201,
    "text": "北银金融科技有限责任公司\r北银金科发〔2022］11号\r关于印发《北银金融科技有限责任公司\r员工考勤请假管理制度》的通知\r各部门：\r为保障员工权益，维护正常工作秩序，提高运营效率，加强\r绩效管理，根据国家、地方有关法律法规，结合公司实际，制定\r本制度。请全体员工遵照执行。\r北银金融科技有限责任公\r科\r2022年\r年月\r区\r（联系人：孙然\r联系电话：010-86373059)\r北银金融科技有限责任公司\r2022年4月22日印发",
    "pages":[
        {
            "number": 1,
            "text": "北银金融科技有限责任公司\r北银金科发〔2022］11号\r关于印发《北银金融科技有限责任公司\r员工考勤请假管理制度》的通知\r各部门：\r为保障员工权益，维护正常工作秩序，提高运营效率，加强\r绩效管理，根据国家、地方有关法律法规，结合公司实际，制定\r本制度。请全体员工遵照执行。\r北银金融科技有限责任公\r科\r2022年\r年月\r区\r（联系人：孙然\r联系电话：010-86373059)\r北银金融科技有限责任公司\r2022年4月22日印发"
        }
    ]
}
```

#### 异步回调

- 创建任务

```python

filename = "tests/cases/pdf2txt/1.png"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2text"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "callback": "http://callback"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")

# $ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2text?taskId=test2&callback=http://callback' --form 'file=@./tests/cases/pdf2txt/1.png' 

# 响应报文
response = {
    "taskId": "test2",
    "status": "waitting",
    "message": "Task accepted",
    "bizType": "pdf2text",
    "fileName": None,
}
```

- 任务执行状态更新回调
```json
{
    "taskId": "test2",
    "status": "running",
    "message": "Task Running",
    "bizType": "pdf2text",
    "fileName": null,
}
```

- 任务执行错误回调

```json
{
    "taskId": "test2",
    "status": "error",
    "message": "错误信息",
    "bizType": "pdf2text",
    "fileName": null,
}

```
- 任务执行成功回调

form file字段保存文件

```json
{
    "taskId": "test2",
    "status": "success",
    "message": "Task success",
    "bizType": "pdf2text",
    "fileName": "",
    "file": "解析结果文件对象",
}
```

## 二、PDF转word(版面复原)

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdf2word
```

#### 京智大脑

```bash
POST http://onlineapp.aip.bj.bob.test:8080/characterRecognition/pdf2x/api/v1/ocr/pdf2word

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE 71A43DABAE7749C6ADB849709B86FB5 |
```

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| outformat | txt/json  |  返回保文格式 调用不传就默认txt|
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |
| ocr | auto/false/true | 是否使用ocr,默认为auto; false表示为标准PDF; true表示OCR解析 |

#### Form Parameter

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | pdf | pdf文件 |

### 返回参数

#### 状态码

| status | message |
| ------ | ------- |
| create | 任务创建完成 |
| success | 任务结束，执行成功|
| error  | 任务结束，执行失败 |
| waitting | 任务等待中 |
| running  | 任务执行中 |
| full | 等待队列已满,系统繁忙,不能够添加新的任务|
| existed | 已存在 |

#### 同步请求示例

```python

filename = "tests/cases/pdf2ppt/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2word"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "async": "false", "callback": "disable"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
with open("tests/a.docx", 'wb') as f:
    f.write(response.content)

```

#### 异步回调

- 创建任务

```python

filename = "tests/cases/pdf2ppt/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2word"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test_pdf2word_2", "callback": "http://callback"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")

# $ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2word?taskId=test_pdf2word_2&callback=http://callback' --form 'file=@./tests/cases/pdf2ppt/test1.pdf' 

# 响应报文
response = {
    "taskId": "test2",
    "status": "waitting",
    "message": "Task accepted",
}
```

- 任务执行状态更新回调
```json
{
    "taskId": "test2",
    "status": "running",
    "message": "Task Running",
}
```

- 任务执行错误回调

```json
{
    "taskId": "test2",
    "status": "error",
    "message": "错误信息",
}

```
- 任务执行成功回调

解析结果为word文件。word文件通过form file字段回调

```json
{
    "taskId": "test2",
    "status": "success",
    "message": "Task success",
    "file": "解析结果文件对象"
}
```

## 三、PDF转excel

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdf2excel
```

#### 京智大脑对接参数

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/pdf2x/api/v1/ocr/pdf2excel

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE F7CA53BD073CFF6604C4CCB9C5F7926D |
```

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| extractor | all/only_table  |  all表示全部输出, only_table表示只输出表格,默认为all   |
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |
| ocr | auto/false/true | 是否使用ocr,默认为auto; false表示为标准PDF; true表示OCR解析 |

#### Form Parameter

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | pdf | pdf文件 |

### 返回参数

#### 状态码

| status | message |
| ------ | ------- |
| create | 任务创建完成 |
| success | 任务结束，执行成功|
| error  | 任务结束，执行失败 |
| waitting | 任务等待中 |
| running  | 任务执行中 |
| full | 等待队列已满,系统繁忙,不能够添加新的任务|
| existed | 已存在 |

#### 同步请求示例

```python

filename = "tests/cases/pdf2excel/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2excel"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "async": "false", "callback": "disable"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
with open("tests/a.pptx", 'wb') as f:
    f.write(response.content)

```

#### 异步回调

- 创建任务

```python

filename = "tests/cases/pdf2excel/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2excel"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test_pdf2excel_2", "callback": "http://callback"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")

# $ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2ppt?taskId=test_pdf2ppt_2&callback=http://callback' --form 'file=@./tests/cases/pdf2ppt/test1.pdf' 

# 响应报文
response = {
    "taskId": "test_pdf2excel_2",
    "status": "waitting",
    "message": "Task accepted",
}
```

- 任务执行状态更新回调
```json
{
    "taskId": "test_pdf2excel_2",
    "status": "running",
    "message": "Task Running",
}
```

- 任务执行错误回调

```json
{
    "taskId": "test_pdf2excel_2",
    "status": "error",
    "message": "错误信息",
}

```
- 任务执行成功回调

解析结果为pptx文件。pptx文件通过form file字段回调

```json
{
    "taskId": "test_pdf2excel_2",
    "status": "success",
    "message": "Task success",
    "file": "解析结果文件对象"
}
```

## 四、PDF转PPT

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdf2ppt
```

#### 京智大脑对接参数

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/pdf2x/api/v1/ocr/pdf2ppt

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE 7A59FD42553B7C85CB9AF127FABBD3E5 |
```

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| taskId | string | 可选参数,上游流水id，如果不传，异步任务会返回自动生成的id          |
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |

#### Form Parameter

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | pdf | pdf文件 |

### 返回参数

#### 状态码

| status | message |
| ------ | ------- |
| create | 任务创建完成 |
| success | 任务结束，执行成功|
| error  | 任务结束，执行失败 |
| waitting | 任务等待中 |
| running  | 任务执行中 |
| full | 等待队列已满,系统繁忙,不能够添加新的任务|
| existed | 已存在 |

#### 同步请求示例

```python

filename = "tests/cases/pdf2ppt/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2ppt"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "async": "false", "callback": "disable"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
with open("tests/a.pptx", 'wb') as f:
    f.write(response.content)

```

#### 异步回调

- 创建任务

```python

filename = "tests/cases/pdf2ppt/test1.pdf"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2ppt"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test_pdf2ppt_2", "callback": "http://callback"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")

# $ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2ppt?taskId=test_pdf2ppt_2&callback=http://callback' --form 'file=@./tests/cases/pdf2ppt/test1.pdf' 

# 响应报文
response = {
    "taskId": "test_pdf2ppt_2",
    "status": "waitting",
    "message": "Task accepted",
}
```

- 任务执行状态更新回调
```json
{
    "taskId": "test_pdf2ppt_2",
    "status": "running",
    "message": "Task Running",
}
```

- 任务执行错误回调

```json
{
    "taskId": "test_pdf2ppt_2",
    "status": "error",
    "message": "错误信息",
}

```
- 任务执行成功回调

解析结果为pptx文件。pptx文件通过form file字段回调

```json
{
    "taskId": "test_pdf2ppt_2",
    "status": "success",
    "message": "Task success",
    "file": "解析结果文件对象"
}
```

## 五、企业流水识别

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/enterprise2excel
```

#### 京智大脑(终端内)

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/ocr-gerenliushui/api/v1/ocr/enterprise2excel

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE F7CA53BD073CFF6604C4CCB9C5F7926D |
```

### 请求参数

#### Query Parameter

| Field    | Type                 | Description                                  |
| -------- | -------------------- | -------------------------------------------- |
| filename | string               | 银行名称（如：中国交通银行（china_traffic_bank），传值需要传英文名称） |


银行字段说明：

| 银行中文名称   | 银行英文名                 | 支持情况 |
| -------- | --------------------------- | ---------|
| 中国交通银行   | china_traffic_bank          | 是 |
| 宁波银行     | ningbo_bank                 | 是 |
| 上海银行     | shanghai_bank               | 是 |
| 中国建设银行   | china_construction_bank     | 是 |
| 中信银行     | citic_bank                  | 是 |
| 兴业银行     | xingye_bank                 | 是 |
| 上海农村商业银行 | shanghai_rural_commercebank | 否|
| 厦门国际银行   | xiamen_international_bank   | 否 | 
| 中国银行     | china_bank                  | 否 |
| 中国农业银行   | china_agricultural_bank     | 否 |
| 中国招商银行   | china_merchants_bank        | 否 |
| 中国工商银行   | china_commercial_bank       | 否 |
| 浦发银行     | pufa_bank                   | 否 |
| 有线表格     | lines_tables                | 是 |


#### Form Parameter

| Field    | Type                 | Description                                  |
| -------- | -------------------- | -------------------------------------------- |
| file     | jpg/png/bmp/jpeg/pdf | 图片或者pdf文件（单张图片或者单页pdf）                       |

#### 请求示例

### 返回参数

#### Success 200

```python
# 返回文件流stream,最终保存为xlsx文件：
with open(xlsx_name,"wb") as file:
    file.write(response.content)
```

## 六、个人流失识别(OCR表格识别)

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/personalbill2excel
```

#### 京智大脑

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/ocr-gerenliushui/api/v1/ocr/personalbill2excel

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE F7CA53BD073CFF6604C4CCB9C5F7926D |
```

### 请求参数

#### Query Parameter

| Field    | Type                 | Description                        |
| -------- | -------------------- | ---------------------------------- |
| filename | string               | 银行名称（如：中国银行（china_bank），传值需要传英文名称） |

| 银行中文名称   | 银行英文名                   | 支持状态 | 
| -------- | ------------------------------ | ----
| 中国交通银行   | china_traffic_bank          | 否 |
| 宁波银行     | ningbo_bank                  | 否 |
| 上海银行     | shanghai_bank                |  否|
| 中国建设银行   | china_construction_bank    | 否 |
| 中信银行     | citic_bank                   | 否 |
| 兴业银行     | xingye_bank                  | 否 |
| 上海农村商业银行 | shanghai_rural_commercebank | 否|
| 厦门国际银行   | xiamen_international_bank   | 否|
| 中国银行     | china_bank                  | 是 |
| 中国农业银行   | china_agriculture_bank      | 是 |
| 中国招商银行   | china_merchants_bank        | 是 |
| 中国工商银行   | china_commercial_bank       | 是 |
| 浦发银行     | pufa_bank                   | 否 |
| 有线表格     | lines_tables                | 是 |

#### Form Parameter 

| Field    | Type                 | Description                        |
| -------- | -------------------- | ---------------------------------- |
| file     | jpg/png/bmp/jpeg/pdf | 图片或者pdf文件（单张图片或者单页pdf）             |

### 响应参数

#### Success 200

```python
# 返回文件流stream,最终保存为xlsx文件：
with open(xlsx_name,"wb") as file:
    file.write(response.content)
```

## 七、OCR个贷催收文书识别

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/personaloan2rec
```

#### 京智大脑

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/ocr-persionallocans/api/v1/ocr/personaloan2rec

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE 071AFFBB116630336EBCA768F6E6B313 |
```

### 请求参数

#### Form Parameter (body param)

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | jpg/png/bmp/jpeg/pdf | 图片或者pdf文件（单张图片或者单页pdf） |

### 响应参数

#### Success 200

```python
返回json格式
{
    "status": 201,
    "content": {

        # 借据详情字段
        "issuing_agency":"城市副中心", # 出账机构
        "contract_text_number":"12312121212", # 合同文本编号
        "customer_name":"XXX有限公司", # 客户名称
        "loan_balance":"111111", # 贷款余额
        "overdue_balance":"12121", # 其中：逾期余额
        #（授权）合同信息字段
        "authorization_contract_text_number":"0610P15******", # 合同文本编号
        # 保证担保合同信息字段
        "guarantee_guarantor_name":["北京安杰码生物科技有限公司","刘玉香"，"金子忆","高昆"],
        # 抵押担保合同信息字段
        "mortgage_guarantor_name":["高昆"],
        # 质押担保合同信息字段
        "pledge_guarantor_name":["***"]

    }
}
```

## 八、图像识别中英文翻译-图像识别路由(img2rec)

### 服务地址

#### 京智大脑对接参数

```bash
POST http://onlineapp.aip.bj.bob.test:8088/characterRecognition/ocr-gerenliushui/api/v1/ocr/img2rec

Headers

| Key           | Value                                       |
| ------------- | ------------------------------------------- |
| Authorization | ACCESSCODE F7CA53BD073CFF6604C4CCB9C5F7926D |
```

### 请求参数

#### Parameter (body param)

| Field | Type                 | Description            |
| ----- | -------------------- | ---------------------- |
| file  | jpg/png/bmp/jpeg/pdf | 图片或者pdf文件（单张图片或者单页pdf） |

### 响应参数

#### Success 200

```python
返回json格式
{
    "status": 201,
    "text": "北银金融科技有限责任公司\n北银金科发〔2022］11号\n关于印发《北银金融科技有限责任公司\n员工考勤请假管理制度》的通知"##### 中英文翻译接口：
```

## 九、PDF多页文字识别

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdf2txt
```

#### 云平台

```bash
POST http://10.56.126.14.30196/api/v1/ocr/pdf2txt
```
### 请求参数

#### Query Parameter

| Field    | Type         | Description                                    |
| -------- | ------------ | ---------------------------------------------- |
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式 |

#### Form Parameter

| Field | Type | Description                  |
| ----- | ---- | ---------------------------- |
| file  | pdf  | 仅支持PDF文件，支持多页，返回不同页之间用 \n 区分 |

### 响应参数

- 返回json格式
- Success 200

```python
{
    "text": "北银金融科技有限责任公司\r北银金科发〔2022］11号\r关于印发《北银金融科技有限责任公司\r员工考勤请假管理制度》的通知\r各部门：\r为保障员工权益，维护正常工作秩序，提高运营效率，加强\r绩效管理，根据国家、地方有关法律法规，结合公司实际，制定\r本制度。请全体员工遵照执行。\r北银金融科技有限责任公\r科\r2022年\r年月\r区\r（联系人：孙然\r联系电话：010-86373059)\r北银金融科技有限责任公司\r2022年4月22日印发"
}
```


## 十、PDF解析接口

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/pdfparser
```

#### 京智大脑对接参数

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| outformat | zip/md/html/json/docx/excel  |  返回保文格式 调用不传就默认json   |
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |

#### Form Parameter (body param)

| Field      | Type                         | Description            |
| ---------- | ---------------------------- | ---------------------- |
| file       | pdf         | 仅支持PDF文件 |

### 返回参数

#### 状态码

| status | message |
| ------ | ------- |
| create | 任务创建完成 |
| success | 任务结束，执行成功|
| running  | 任务执行中 |
| error  | 任务结束，执行失败 |
| waitting | 任务等待中 |
| full | 等待队列已满,系统繁忙,不能够添加新的任务|
| existed | 已存在 |

#### 同步请求示例

```python
filename = "tests/cases/pdf2txt/1.png"
url = "http://127.0.0.1:8000/api/v1/ocr/pdfparser"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "outformat": "json"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
```
```bash
$ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdfparser?taskId=test2&outformat=json' --form 'file=@./tests/cases/pdf2txt/1.png' 
```

```python
{
    "pdf_info": null,
    "pdf_outline": null,
    "fonts": {},
    "images": {},
    "pages":[],
    "execute":{}
}
```

#### 异步回调

- 创建任务

```python

filename = "tests/cases/pdf2txt/1.png"
url = "http://127.0.0.1:8000/api/v1/ocr/pdf2text"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"testId": "test2", "callback": "http://callback"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")

# $ crul --location 'http://127.0.0.1:8000/api/v1/ocr/pdf2text?taskId=test2&callback=http://callback' --form 'file=@./tests/cases/pdf2txt/1.png' 

# 响应报文
response = {
    "taskId": "test2",
    "status": "waitting",
    "message": "Task accepted",
    "bizType": "pdf2text",
    "fileName": None,
}
```

- 任务执行状态更新回调
```json
{
    "taskId": "test2",
    "status": "running",
    "message": "Task Running",
    "bizType": "pdf2text",
    "fileName": null,
}
```

- 任务执行错误回调

```json
{
    "taskId": "test2",
    "status": "error",
    "message": "错误信息",
    "bizType": "pdf2text",
    "fileName": null,
}

```
- 任务执行成功回调

form file字段保存文件

```json
{
    "taskId": "test2",
    "status": "success",
    "message": "Task success",
    "bizType": "pdf2text",
    "fileName": "",
    "file": "解析结果文件对象",
}
```

# 提取需求

## 回单+信汇信息提取算法服务

## 持仓分析

### 服务地址

#### 金科-云桌面

```bash
POST http://172.16.5.161:9111/api/v1/ocr/holding_analysis
```

#### 京智大脑对接参数

### 请求参数

#### Query Parameter

| Field  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| bodyformat | zip/md/html/json/docx/excel  |  返回保文格式 调用不传就默认json   |
| async    | false / true | 是否开启同步或异步, 默认是true                             |
| callback | string       | 回调接口地址, 必须以http或https开头, 设置callback有值时，默认为异步方式,回调请求以form方式file发送文件 |

#### Form Parameter (body param)

| Field      | Type                         | Description            |
| ---------- | ---------------------------- | ---------------------- |
| file       | pdf         | 仅支持PDF文件 |

### 返回参数

#### Success 200

同步请求示例：

```python

filename = "tests/cases/holding_case/001.jpg"
url = "http://127.0.0.1:8000/api/v1/ocr/holding_analysis"
files = {
    "file": (filename, open(filename, "rb")),
}
params = {"async": "false"}
response = requests.post(url, params=params, files=files)
assert response.status_code == 200, response.content
print(f"{response.url=},{len(response.content)=}")
# with open("tests/a.md", 'wb') as f:
#     f.write(response.content)

```

- bodyformat=json 默认格式
- 请求地址示例： http://127.0.0.1:8000/api/v1/ocr/holding_analysis

返回结构体:


| id  | Type         | Description                    |
| ------ | ------------ | ------------------------------ |
| code	                            |   int	         |  业务查询状态，200为调用接口成功 |
| message                           |	string	     |  返回状态描述                    |
| data.text                         |	string	     |  回复答案                        |
| data.total_data                   |	dict         |	总部分                          |
| data.total_data.tot_asset         |	float        |	总资产                          |
| data.total_data.tot_return        |	float	     |  总盈亏比例                      |
| data.total_data.tot_return_amount |	float	     |  总盈亏                          |
| data.holding_data                 |	list[dict]   |	分项                            |
| data.holding_data.name            |	string	     |  证券名称                        |
| data.holding_data.code            |	string	     |  证券代码                        |
| data.holding_data.amount          |	float	     |  投资金额                        |
| data.holding_data.ret             |	float	     |  盈亏金额                        |
| data.holding_data.shares          |	float	     |  份额数量                        |
| data.holding_data.cost            |	float	     |  成本价格                        |
| data.holding_data.pchg            |	float	     |  盈亏比例                        |
| data.holding_data.ratio           |	string	     |  总资产占比                      |


```json
{
    "id": "",
    "code": 200,
	"data": {
        "text": "我是识别的文字",
        "total_data": {
            "tot_asset": 222220,
            "tot_return": -3.5,
            "tot_return_amount": -333
        },
        "holding_data": [
            {
                "name": "中国平安",
                "code": "601318",
                "amount": 22342,
                "ret": -322,
                "cost": 15,
                "pchg": -3.5,
                "shares":1000,
                "ratio": "95%"
            },
            {
                "name": "中国医药",
                "code": "600056",
                "amount": 3323,
                "ret": 333,
                "cost": 9,
                "pchg": 3.3,
                "shares":1000,
                "ratio": "5%"
            }
        ]
    }
}
```
