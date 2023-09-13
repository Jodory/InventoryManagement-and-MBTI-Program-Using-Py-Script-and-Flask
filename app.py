from flask import Flask
from flask import request, render_template, redirect, flash, session
from math import ceil
import dbController as dc
import main.convertRawDataToList as crl
import main.makeReportTable as mrt
import main.getDateList as gdl
from datetime import datetime
# Flask 객체 생성
app = Flask(__name__)
#flash secret_key
app.config["SECRET_KEY"] = "sh291hfwnh8@hwqjh2(*@#*Uh2N2920hF@H0Fh@C293"
allList = dc.get_excellist()
errorList = []
releaseList = []

# 인덱스 페이지
@app.route('/')
def index():
    return render_template('./pyscript/index.html', introduction = "2022 프로그래밍응용 프로젝트", title = "Programming Application Project")

@app.route('/start', methods=['GET', 'POST'])
def start():  # put application's code here
    if request.method == 'POST':
        id = request.form.get("id")
        pwd = request.form.get("pwd")

        if id == '' or pwd == '':
            flash("아이디와 비밀번호를 입력해주세요.")
            return render_template("./main/login.html")

        if id == "admin" and pwd == "1234":
            session['userid'] = "manager"
            flash("관리자님, 안녕하세요!")
            return render_template("./main/login.html")
        elif id == "user" and pwd == "1234":
            session['userid'] = "user"
            flash("사용자님, 안녕하세요!")
            return render_template("./main/login.html")
        elif id == "manager":
            flash("비밀번호가 잘못되었습니다.")
            return render_template("./main/login.html")
        elif id == "user":
            flash("비밀번호가 잘못되었습니다.")
            return render_template("./main/login.html")

        else:
            flash("아이디 혹은 비밀번호가 잘못되었습니다.")
            return render_template("./main/login.html")
    else:
        return render_template("./main/login.html")

@app.route('/aboutPyscript')
def aboutPyscript():
  return render_template('./pyscript/aboutPyscript.html', title = 'Pyscript란?')

@app.route('/hw1')
def hw1():
  return render_template('./pyscript/hw1.html', title = 'HW1')

@app.route('/hw1El')
def hw1El():
  title = request.args.get('title', "HW1")
  return render_template('./pyscript/hw1El.html', title = title)

@app.route('/hw2')
def hw2():
  return render_template('./pyscript/hw2.html', title = 'HW2')

@app.route('/hw2El')
def hw2El():
  title = request.args.get('title', "HW2")
  return render_template('./pyscript/hw2El.html', title = title)  

@app.route('/mbti')
def mbti():
  return render_template('./pyscript/mbti.html', title = 'MBTI')

@app.route('/mbti_result', methods=['GET', 'POST'])
def mbti_result():
    mbti = []
    result = []
    if request.method == 'POST':
        ans = request.form.get("ans")
        for i in range(1, 5):
            mbti.append(request.form.get(f'{i}'))
        if mbti.count("e") >= mbti.count("i"):result.append("E")
        else:result.append("I")
        
        if mbti.count("s") >= mbti.count("n"):result.append("S")
        else:result.append("N")

        if mbti.count("t") >= mbti.count("f"):result.append("T")
        else:result.append("F")

        if mbti.count("j") >= mbti.count("p"):result.append("J")
        else:result.append("P")

        getResult = ''.join(result) + '.txt'
        explains = []
        f = open("./static/py/"+getResult, 'r')
        lines = f.readlines()
        for line in lines:
            explains.append(line.rstrip())
        f.close()
        result = ''.join(result)
        detail = 'https://www.16personalities.com/ko/성격유형-' + result
    return render_template('./pyscript/mbti_result.html', title = 'MBTI', ans = ans, result = result, explains = explains, detail = detail)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid',None)
    return redirect('/')

@app.route('/main')
def main_page():
    return render_template("./main/main.html")

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == "GET":
        return render_template("./main/inventory.html", excelList=allList)
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해 주세요.\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        if int(sd) > int(ed):
            return "<script>alert(\'시작일이 종료일보다 클 수 없습니다.\')\nwindow.history.back()</script>"
        data = dc.select_by_date(sd, ed)
        return render_template("./main/inventory.html", excelList=data, startdate=str(startdate), enddate=str(enddate))


# 바코드 읽기
@app.route('/readBarcode', methods=['GET', 'POST'])
def read_barcode():
    if request.method == 'GET':
        return render_template("./main/readBarcodeString.html")
    else:
        # GET이 아닌 request (확인submit)
        rawBarcodeData = request.form.get("barcode")
        if rawBarcodeData != "" and rawBarcodeData is not None:
            blist = crl.convert(rawBarcodeData)
            # time부분 나중에 함수로 빼기
            dc.append_raw_barcodes(blist)
            dc.printingLabel(blist)
        #최근순으로 모든 raw바코드열 가져오기
        return render_template("./main/readBarcodeString.html")

# 출고 바코드 찍기
@app.route('/releaseEngine', methods=['GET', 'POST'])
def release_engine():
    if request.method == 'GET':
        ## 미리 전역 변수에 로드
        global errorList
        errorList = dc.get_error_engine_list()
        return render_template("./main/releaseEngine.html", el=releaseList, length=len(releaseList))
    else:
        barcode = request.form.get("barcode")
        ## 바코드 유효성 체크
        if barcode != "" and len(barcode) == 16:
            #에러 엔진 리스트에 포함된 엔진이면
            eid = barcode[6:12]
            for i in errorList:
                #eid가 같으면, 불출x
                if eid == i[2]:
                    print("error : ", eid)
                    return render_template("./main/releaseEngine.html", el=releaseList, length=len(releaseList))
            #정상 엔진
            print("불출 : ", eid)
            if barcode not in releaseList:
                releaseList.append(barcode)
        return render_template("./main/releaseEngine.html", el=releaseList, length=len(releaseList))


# 보유 엔진 보고서
@app.route('/report', methods=['GET', 'POST'])
def holding_engines_report():
    #test dates
    if request.method == 'GET':
        return render_template("./main/report.html", table="<p>날짜를 선택해주세요.</p>")
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해 주세요.\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        if int(sd) > int(ed):
            return "<script>alert(\'시작일이 종료일보다 클 수 없습니다.\')\nwindow.history.back()</script>"
        dates = gdl.datelist(sd, ed)
        table = mrt.make(dc.select_all_for_report(allList, dates[0]), dates)
        return render_template("./main/report.html", table=table, startdate=str(startdate), enddate=str(enddate))


# dailylist
@app.route('/dailylist')
def daily_engine_list():
    inputList = []
    outputList = []
    today = dc.get_today_date()
    for i in range(0, len(allList)):
        if allList[i][3] == today:
            inputList.append(allList[i])
        elif allList[i][5] == today:
            outputList.append(allList[i])
    inputlen = len(inputList)
    outputlen = len(outputList)
    return render_template("./main/dailylist.html", inputList = inputList, inputlen = inputlen, outputList = outputList, outputlen = outputlen)


# mip 추가
@app.route('/addMIP', methods=['GET', 'POST'])
def add_mip_type():
    if request.method == 'GET':
        tmpList = dc.get_type_list()
        mipList = []
        for i in tmpList[::-1]:
            mipList.append(i)

        return render_template("./main/addMIP.html", mipList = mipList)
    else:
        tmpList = []
        mipList = []
        mip = request.form.get("mip")
        type = request.form.get("type")
        if mip == "" and mip is None:
            return render_template("./main/addMIP.html")
        if type == "" and type is None:
            return render_template("./main/addMIP.html")
        if len(mip) != 4:
            return render_template("./main/addMIP.html")
        dc.add_MIP(mip, type)
        tmpList = dc.get_type_list()
        for i in tmpList[::-1]:
            mipList.append(i)
        return render_template("./main/addMIP.html", mipList = mipList)

#에러엔진 설정
@app.route('/setInvalidEngine', methods=['GET', 'POST'])
def set_invalid_engine_exp():
    errorList = []
    if request.method == 'GET':
        curErrorList = dc.get_error_engine_list()
        mount = len(curErrorList)
        return render_template("./main/setInvalidEngine.html", curErrorList=curErrorList, errorMount=mount)
    else:
        eng = request.form.getlist("ENG[]")
        exp = request.form.getlist("EXP[]")
        errorList = dc.set_invalid_engine(eng, exp)
        errorEngine = '입력 에러 엔진: '

        # 잘못된 리스트가 있는경우
        if len(errorList) != 0:
            for eng in errorList:
                errorEngine = errorEngine + eng + ' '
            flash(errorEngine)

        curErrorList = dc.get_error_engine_list()
        mount = len(curErrorList)
        return render_template("./main/setInvalidEngine.html", errorList = errorList, curErrorList=curErrorList, errorMount=mount)


#동기화
@app.route('/refresh')
def refresh():
    dc.synchronization()
    print("동기화 완료")
    return "<script>alert(\'동기화 완료\')\nwindow.history.back()</script>"


#출고, 출고리스트의 엔진들을 출고시키고, 출고리스트를 초기화
@app.route('/release')
def release():
    global releaseList
    a = dc.delete_rows(releaseList)
    releaseList = []
    if a >= 0:
        return "<script>alert(\'출고 완료, "+str(a)+"개 엔진이 출고되었습니다.\')\nwindow.location.href='/main'</script>"
    elif a == -2:
        return "<script>alert(\'출고 에러, 존재하지 않는 엔진이 있습니다.\')\nwindow.location.href='/main'</script>"
    elif a == -3:
        return "<script>alert(\'출고 에러, 이미 불출된 엔진이 있습니다.\')\nwindow.location.href='/main'</script>"
    else:
        return "<script>alert(\'출고 에러, File Error\')\nwindow.location.href='/main'</script>"



@app.route('/inventoryPayment', methods=['GET', 'POST'])
def inventory_payment():
    global allList
    if request.method == "GET":
        startdate, enddate = datetime.now(), datetime.now()
        startdate, enddate = str(startdate), str(enddate)
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        check, paymentList = dc.inventory_payment(allList, sd, ed)
        return render_template("./main/inventoryPayment.html", paymentList=paymentList)
    else:
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        if len(startdate) < 10 or len(enddate) < 10:
            return "<script>alert(\'날짜를 선택해주세요\')\nwindow.history.back()</script>"
        sd = str(startdate[0:4] + startdate[5:7] + startdate[8:10])
        ed = str(enddate[0:4] + enddate[5:7] + enddate[8:10])
        check, paymentList = dc.inventory_payment(allList, sd, ed)

        if check == False:
            return "<script>alert(\'" + paymentList + "엔진의 Type, MIP 가 DB에 추가되어있지 않습니다." + "\')\nwindow.history.back()</script>"
        elif check == True:
            return render_template("./main/inventoryPayment.html", paymentList=paymentList)

        return render_template("./main/inventoryPayment.html", paymentList=paymentList)

@app.route('/dailylist_worker', methods=['GET', 'POST'])
def dailylist_worker():
    return render_template("./main/dailylist_worker.html")


# flask 구동 (main)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)