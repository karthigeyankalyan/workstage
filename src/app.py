from datetime import datetime

from datetime import timedelta

import pymongo

import os

import codecs

import gridfs

from bson import json_util

from bson.objectid import ObjectId

from flask import Flask, render_template, request, session, json, abort

from src.common.database import Database
from src.models.scheme import Scheme

from src.models.work import Work

from src.models.stage import Stage

from src.models.users import User

app = Flask(__name__)  # main

app.secret_key = "commercial"


@app.before_first_request

def initialize_database():

    Database.initialize()


@app.route('/')

def home():
    # remote_address = request.headers.getlist("X-Forwarded-For")[0]

    return render_template('home.html')


@app.route('/login')

def login_form():

    return render_template('login.html')


@app.route('/register')

def register_form():

    return render_template('register.html')

@app.route('/profile_landing')

def profile():

    email = session['email']

    user = User.get_by_email(email)

    if email:

        if user.designation == 'HQ Staff':

            return render_template('profile_HQ.html', user=user)

        else:

            return render_template('profile_blocks.html', user=user)

    else:

        return render_template('login_fail.html')


@app.route('/authorize/login', methods=['POST'])

def login_user():

    email = request.form['email']

    password = request.form['password']

    valid = User.valid_login(email, password)

    User.login(email)

    user = User.get_by_email(email)

    if valid:

        if user.designation == 'HQ Staff':

            return render_template('profile_HQ.html', user=user)


        else:

            return render_template('profile_blocks.html', user=user)

    else:

        return render_template('login_fail.html')

@app.route('/authorize/register', methods=['POST'])

def register_user():

    email = request.form['email']

    password = request.form['password']

    username = request.form['username']

    designation = request.form['designation']

    block = request.form['block']

    User.register(email, password, username, designation, block)

    user = User.get_by_email(email)

    if user.designation == 'HQ Staff':

        return render_template('profile_HQ.html', user=user)

    else:

        return render_template('profile_blocks.html', user=user)
    
@app.route('/add_work/<string:user_id>', methods=['POST', 'GET'])

def work_form(user_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':

            user = User.get_by_id(user_id)

            return render_template('add_work.html', user=user)

        else:

            user = User.get_by_id(user_id)
            amount = request.form['amount']
            block = request.form['Blocks']
            panchayat = request.form['panchayat']
            habitation = request.form['habitation']
            total_stages = int(request.form['totalstages'])
            start_date = request.form['startdate']
            end_date = request.form['enddate']
            work_name = request.form['workname']
            scheme_group_name = request.form['schemegroupname']
            scheme_name = request.form['schemename']
            work_group_name = request.form['workgroupname']
            work_type = request.form['worktype']
            user_id = user_id
            user_name = user.username

            work = Work(amount=amount, block=block, scheme_group_name = scheme_group_name, scheme_name=scheme_name,
                        work_group_name=work_group_name, work_type=work_type, panchayat=panchayat, habitation=habitation,
                        total_stages=total_stages, start_date=start_date,
                        user_id=user_id, user_name=user_name, work_status="Open", work_name=work_name,
                        end_date=end_date)

            work.save_to_mongo()

            print(total_stages)

            for i in range(int(total_stages)):

                print(total_stages)

                stage_name_string = "sn" + str(i)

                stage_amount_string = "sa" + str(i)

                stage_order_id_string = "soi" + str(i)

                stage_start_date_string = "ssd" + str(i)

                stage_end_date_string = "sed" + str(i)

                stage_name = request.form[stage_name_string]

                stage_amount = request.form[stage_amount_string]

                stage_order_id = request.form[stage_order_id_string]

                stage_start_date = request.form[stage_start_date_string]

                stage_end_date = request.form[stage_end_date_string]

                work_id = work.work_id

                application = Stage(stage_name=stage_name, start_date=stage_start_date,

                                    end_date=stage_end_date, amount=stage_amount, total_stages=total_stages, work_name=work_name,

                                    user_name=user_name, user_id=user_id, stage_order_id=stage_order_id, work_id = work_id)

                application.save_to_mongo()

            if user.designation == 'HQ Staff':

                   return render_template('application_added.html', work=work, user=user)

            else:
                   return render_template('application_added_blocks.html', work=work, user=user)

    else:

        return render_template('login_fail.html')


@app.route('/add_scheme/<string:user_id>', methods=['POST', 'GET'])

def scheme_form(user_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':

            user = User.get_by_id(user_id)

            return render_template('add_scheme.html', user=user)

        else:

            user = User.get_by_id(user_id)

            scheme_group_name = request.form['schemegroupname']

            scheme_name = request.form['schemename']

            work_group_name = request.form['workgroupname']

            work_type = request.form['worktype']

            scheme = Scheme(scheme_group_name=scheme_group_name, scheme_name=scheme_name,

                        work_group_name = work_group_name, work_type = work_type)

            scheme.save_to_mongo()

            if user.designation == 'HQ Staff':

                return render_template('application_added.html', scheme=scheme, user=user)

            else:
                return render_template('application_added_blocks.html', scheme=scheme, user=user)

    else:

            return render_template('login_fail.html')

@app.route('/updatework/<string:work_id>', methods=['POST', 'GET'])

def update_work(work_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':

            user = User.get_by_email(email)

            if user.designation == 'HQ Staff':

                   return render_template('update_work_form.html', user=user, work_id=work_id)

            else:

                   return render_template('update_work_form_blocks.html', user=user, work_id=work_id)
        else:

            user = User.get_by_email(email)

            amount = request.form['amount']

            block = request.form['Blocks']

            work_status = request.form['workstatus']

            total_stages = request.form['totalstages']

            panchayat = request.form['panchayat']

            habitation = request.form['habitation']

            start_date = request.form['startdate']

            end_date = request.form['enddate']

            work_name = request.form['workname']

            amount_spent = request.form['amountspent']

            scheme_group_name = request.form['schemegroupname']

            scheme_name = request.form['schemename']

            work_group_name = request.form['workgroupname']

            work_type = request.form['worktype']

            user_id = user._id

            user_name = user.username

            start_date = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                                            datetime.now().time())

            end_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                                           datetime.now().time())

            Work.update_work(amount=amount, block=block, amount_spent = amount_spent,  scheme_group_name = scheme_group_name,

                        scheme_name=scheme_name, panchayat=panchayat, habitation=habitation,

                        work_group_name=work_group_name, work_type=work_type,

                        total_stages=total_stages, start_date=start_date,

                        user_id=user_id, user_name=user_name, work_id = work_id, work_status=work_status, work_name = work_name,

                        end_date=end_date)

            Stage.update_work_name(work_id=work_id, work_name=work_name)

            if user.designation == 'HQ Staff':

                   return render_template('application_added.html', user=user)

            else:

                   return render_template('application_added_blocks.html', user=user)

    else:

        return render_template('login_fail.html')


@app.route('/add_stage/<string:work_id>', methods=['POST', 'GET'])

def add_stage(work_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':

            user = User.get_by_email(email)

            if user.designation == 'HQ Staff':

                  return render_template('add_stage.html', user=user, work_id= work_id)

            else:

                  return render_template('add_stage_blocks.html', user=user, work_id= work_id)

        else:

            user = User.get_by_email(email)

            stage_name = request.form['stagename']

            start_date = request.form['startdate']

            end_date = request.form['enddate']

            amount = request.form['amount']

            total_stages = request.form['totalstages']

            stage_order_id = request.form['stageorderid']

            user_id = user._id

            user_name = user.username

            work_id = work_id

            application = Stage(stage_name= stage_name, start_date = start_date,

                                end_date = end_date, amount = amount, total_stages = total_stages, stage_status="Open",

                                user_name = user_name, user_id = user_id, stage_order_id = stage_order_id, work_id = work_id)

            application.save_to_mongo()

            if user.designation == 'HQ Staff':

                   return render_template('application_added.html', application=application, user=user)

            else:
                   return render_template('application_added_blocks.html', application=application, user=user)

    else:

        return render_template('login_fail.html')

@app.route('/updatestage/<string:_id>', methods=['POST', 'GET'])

def update_stage(_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':
            user = User.get_by_email(email)
            if user.designation == 'HQ Staff':
                 return render_template('update_stage_form.html', user=user, _id=_id)

            else:

                 return render_template('update_stage_from_blocks.html', user=user, _id=_id)

        else:

            user = User.get_by_email(email)

            amount = request.form['amount']

            stage_name = request.form['stagename']

            stage_order_id = request.form['stageorderid']

            total_stages = request.form['totalstages']

            stage_status = request.form['stagestatus']

            start_date = request.form['startdate']

            end_date = request.form['enddate']

            user_id = user._id

            user_name = user.username

            start_date = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                                            datetime.now().time())

            end_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                                           datetime.now().time())

            application = Database.find("stages", {"_id": _id})

            work_id=None

            for result_object in application[0:1]:

                work_id = result_object['work_id']

            application = Database.find("stages", {"_id": _id})

            stage_status_old = None

            for result_object in application[0:1]:
                stage_status_old = result_object['stage_status']

            if stage_status_old != stage_status and stage_status == 'Close':

                var = int(stage_order_id)+1

                print(work_id, var)

                app = Database.find("stages", {"$and": [{"work_id": work_id}, {"stage_order_id": str(var)}]})

                stage_second_name = None

                for result_object in app[0:1]:
                    stage_second_name = result_object['stage_name']
                    Work.update_current_stage(work_id=work_id, stage_name=stage_second_name, stage_order_id=stage_order_id)

            else:

                var = int(stage_order_id)

                app = Database.find("stages", {"$and": [{"work_id": work_id}, {"stage_order_id": str(var)}]})

                stage_second_name = None

                for result_object in app[0:1]:
                    stage_second_name = result_object['stage_name']
                    var = int(stage_order_id)-1
                    Work.update_current_stage(work_id=work_id, stage_name=stage_second_name,
                                              stage_order_id=str(var))

            print(request.files["Image_upload"])
            for file in request.files.getlist("Image_upload"):
                filename = file.filename

                URI = os.environ['MONGODB_URI']
                client = pymongo.MongoClient(Database.URI)
                DATABASE = client['heroku_thg5d5x0']

                # URI = "mongodb://127.0.0.1:27017"
                # client = pymongo.MongoClient(URI)
                # DATABASE = client['Dindugul']

                fs = gridfs.GridFS(DATABASE)
                #            print(file)
                fileid = fs.put(file, filename=filename)
                #            fileid = fs.put(request.files['Image_upload'].read(), filename=filename)

                DATABASE['road_images'].insert_one({"Image_upload": filename, "fileid": fileid, "stageid": _id})

            Stage.update_stage(amount=amount, stage_name=stage_name,
                        stage_order_id=stage_order_id, total_stages=total_stages, start_date=start_date,
                        user_id=user_id, user_name=user_name, _id =_id, work_id=work_id, stage_status=stage_status,
                        end_date=end_date)

            if user.designation == 'HQ Staff':

                        return render_template('application_added.html', user=user)

            else:

                        return render_template('application_added_blocks.html', user=user)

    else:

        return render_template('login_fail.html')

@app.route('/updatescheme/<string:_id>', methods=['POST', 'GET'])

def update_scheme(_id):

    email = session['email']

    if email is not None:

        if request.method == 'GET':

            user = User.get_by_email(email)

            return render_template('update_scheme_form.html', user=user, _id=_id)

        else:

            user = User.get_by_email(email)

            scheme_group_name = request.form['schemegroupname']

            scheme_name = request.form['schemename']

            work_group_name = request.form['workgroupname']

            work_type = request.form['worktype']

            Scheme.update_scheme(scheme_group_name= scheme_group_name, scheme_name=scheme_name,

                        work_group_name=work_group_name, work_type=work_type, _id=_id)

            return render_template('application_added.html', user=user)

    else:

        return render_template('login_fail.html')

@app.route('/view_work')

def view_work():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if user.designation == 'HQ Staff':

              return render_template('view_work.html', user=user)

        else:

              block = user.block

              return render_template('view_work_blocks.html', user=user, block = block)


    else:

        return render_template('login_fail.html', user=user)

@app.route('/view_scheme')

def view_scheme():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

              return render_template('view_scheme.html', user=user)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/view_work_by_blocks')

def view_work_by_blocks():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

              return render_template('view_work_by_blocks.html', user=user)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/Completed_work')

def Completed_work():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if user.designation == 'HQ Staff':

              return render_template('completed_work.html', user=user)
        else:

              block = user.block

              return render_template('completed_work_blocks.html', user=user, block = block)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/Ongoing_work')

def Ongoing_work():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if user.designation == 'HQ Staff':

              return render_template('ongoing_work.html', user=user)
        else:

              block = user.block

              return render_template('ongoing_work_blocks.html', user=user, block = block)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/Deadline_violation_work')

def Deadline_violation_work():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if user.designation == 'HQ Staff':

              return render_template('deadline_violation_work.html', user=user)
        else:

              block = user.block

              return render_template('deadline_violation_work_blocks.html', user=user, block = block)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/view_stage/<string:work_id>')

def view_stage(work_id):

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if user.designation == 'HQ Staff':

                return render_template('view_stage.html', user=user, work_id=work_id)
        else:

                return render_template('view_stage_blocks.html', user=user, work_id=work_id)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/Overall_summary', methods=['POST', 'GET'])

def Overall_Summary():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if request.method == 'GET':

                   return render_template('between_dates_overall.html', user=user)

        else:

            start_date = request.form['startdate']

            end_date = request.form['enddate']


            return render_template('overall_summary_sheet.html', user=user, start_date=start_date,
                                        end_date=end_date)

    else:

        return render_template('login_fail.html', user=user)

@app.route('/Block_summary', methods=['POST', 'GET'])

def Block_Summary():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if request.method == 'GET':

            if user.designation == 'HQ Staff':

                   return render_template('between_dates_blockwise.html', user=user)
            else:

                return render_template('between_dates_blockwise_blocks.html', user=user)

        else:

            start_date = request.form['startdate']

            end_date = request.form['enddate']

            if user.designation == 'HQ Staff':

                 block = request.form['block']

                 return render_template('blockwise_summary_sheet.html', user=user, start_date=start_date,
                                        end_date=end_date, block=block)

            else:

                block=user.block

                return render_template('blockwise_summary_sheet_blocks.html', user=user, start_date=start_date,
                                       end_date=end_date, block=block)
    else:

        return render_template('login_fail.html', user=user)

@app.route('/Scheme_summary', methods=['POST', 'GET'])

def Scheme_Summary():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

        if request.method == 'GET':

                   return render_template('between_dates_departmentwise.html', user=user)

        else:

            start_date = request.form['startdate']

            end_date = request.form['enddate']

            scheme_group_name = request.form['schemegroupname']

            scheme_name = request.form['schemename']

            work_group_name= request.form['workgroupname']

            work_type= request.form['worktype']

            return render_template('departmentwise_summary_sheet.html', user=user, start_date=start_date,
                                    end_date=end_date, scheme_group_name=scheme_group_name, scheme_name=scheme_name,
                                    work_group_name=work_group_name, work_type=work_type)
    else:

        return render_template('login_fail.html', user=user)

@app.route('/raw_work/<string:work_id>')

def raw_demands_by_work_id(work_id):

    work = []

    work_dict = Database.find("works", {"work_id": work_id})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/raw_stage/<string:_id>')

def raw_demands_by_stage_id(_id):

    stage = []

    stage_dict = Database.find("stages", {"_id": _id})

    for tran in stage_dict:

        stage.append(tran)

    single_stage = json.dumps(stage, default=json_util.default)

    return single_stage

@app.route('/raw_scheme/<string:_id>')

def raw_demands_by_scheme_id(_id):

    scheme = []

    scheme_dict = Database.find("schemes", {"_id": _id})

    for tran in scheme_dict:

        scheme.append(tran)

    single_scheme = json.dumps(scheme, default=json_util.default)

    return single_scheme

@app.route('/WorkBySchemes/<string:scheme_value>')

def get_work_by_scheme(scheme_value):

    work = []

    work_dict = Database.find("works", {"scheme_name": scheme_value})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/WorkBySchemes/<string:block>/<string:scheme_value>')

def get_work_by_scheme_block(block,scheme_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block},
                                                 {"scheme_name": scheme_value}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllWorks/<string:block>')

def view_all_work_blocks(block):

    work = []

    work_dict = Database.find("works",{"block": block})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllWorks/')

def view_all_work():

    work = []

    work_dict = Database.find("works", {})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllSchemes')

def view_all_schemes():

    scheme = []

    scheme_dict = Database.find("schemes", {})

    for tran in scheme_dict:

        scheme.append(tran)

    single_scheme = json.dumps(scheme, default=json_util.default)

    return single_scheme

@app.route('/ViewAllCompletedWorks')

def view_all_completed_work():

    work = []

    work_dict = Database.find("works", {"work_status": "Close"})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllCompletedWorks/<string:block>')

def view_all_completed_work_blocks(block):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block},
                                                 {"work_status": "Close"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllOngoingWorks/<string:block>')

def view_all_ongoing_work_blocks(block):

    work = []

    work_dict = Database.find("works",{"$and": [{"block": block},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllOngoingWorks')

def view_all_ongoing_work():

    work = []

    work_dict = Database.find("works", {"work_status": "Open"})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllDeadlineWorks')

def view_all_deadline_work():

    work = []

    work_dict = Database.find("works", {"$and": [{"end_date": {"$lte": datetime.now()}},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/ViewAllDeadlineWorks/<string:block>')

def view_all_deadline_work_blocks(block):

    work = []

    work_dict = Database.find("works", {"$and": [{"end_date": {"$lte": datetime.now()}}, {"block" : block},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Blocks/<string:block_value>')

def get_work_by_blocks(block_value):

    work = []

    work_dict = Database.find("works", {"block": block_value})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Stagesbywork/<string:work_id>')

def stages_by_work(work_id):

    stage = []

    stage_dict = Database.find("stages", {"work_id": work_id})

    for tran in stage_dict:

        stage.append(tran)

    single_stage = json.dumps(stage, default=json_util.default)

    return single_stage

@app.route('/Completed/<string:block>/<string:scheme_value>')

def get_work_by_completion_block(block,scheme_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"scheme_name": scheme_value}, {"block" : block},

                                                          {"work_status": "Close"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Completed<string:block_value>')

def get_work_by_completion(block_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block_value},

                                                          {"work_status": "Close"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Ongoing/<string:block>/<string:scheme_value>')

def get_work_by_ongoing_block(block,scheme_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block}, {"scheme_name": scheme_value},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Ongoing<string:block_value>')

def get_work_by_ongoing(block_value):

    work = []

    work_dict = Database.find("works", {"$and": [ {"block": block_value},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Deadline<string:block_value>')

def get_work_by_deadline(block_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block_value},
                                                 {"end_date": {"$lte": datetime.now()}},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/Deadline/<string:block>/<string:scheme_value>')

def get_work_by_deadline_blocks(block, scheme_value):

    work = []

    work_dict = Database.find("works", {"$and": [{"block": block}, {"scheme_name": scheme_value},
                                                 {"end_date": {"$lte": datetime.now()}},
                                                 {"work_status": "Open"}]})

    for tran in work_dict:

        work.append(tran)

    single_work = json.dumps(work, default=json_util.default)

    return single_work

@app.route('/BlockReport/<string:start_date>/<string:end_date>')

def block_report(start_date, end_date):

    all_works = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                             datetime.now().time())

    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                           datetime.now().time())

    all_works_dict = Database.find("works", {"end_date": {"$gte": start, "$lt": end}})

    for tran in all_works_dict:

        all_works.append(tran)

    all_w = json.dumps(all_works, default=json_util.default)

    return all_w

@app.route('/SchemeReport/<string:start_date>/<string:end_date>')

def scheme_report(start_date, end_date):

    all_works = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                             datetime.now().time())

    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                           datetime.now().time())

    all_works_dict = Database.find("works", {"end_date": {"$gte": start, "$lt": end}})

    for tran in all_works_dict:

        all_works.append(tran)

    all_w = json.dumps(all_works, default=json_util.default)

    return all_w

@app.route('/BlockFilterByScheme/<string:start_date>/<string:end_date>')

def block_filter_by_scheme(start_date, end_date):

    all_works = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                             datetime.now().time())

    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                           datetime.now().time())

    all_works_dict = Database.find("works",{"end_date": {"$gte": start, "$lt": end}})

    for tran in all_works_dict:

        all_works.append(tran)

    all_w = json.dumps(all_works, default=json_util.default)

    return all_w

@app.route('/BlockReport/<string:start_date>/<string:end_date>/<string:block>')

def Block_report(start_date, end_date, block):

    all_works = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                             datetime.now().time())

    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                           datetime.now().time())

    all_works_dict = Database.find("works", {"$and": [{"end_date": {"$gte": start, "$lt": end}},

                                                        {"block": block}]})

    for tran in all_works_dict:

        all_works.append(tran)

    all_w = json.dumps(all_works, default=json_util.default)

    return all_w

@app.route('/SchemeReport/<string:start_date>/<string:end_date>/<string:scheme_group_name>/<string:scheme_name>/<string:work_group_name>/<string:work_type>')

def Department_report(start_date, end_date, scheme_group_name,scheme_name,work_group_name,work_type):

    all_works = []

    start = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                             datetime.now().time())

    end = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                           datetime.now().time())

    if scheme_group_name== 'All':
        all_works_dict = Database.find("works", {"end_date": {"$gte": start, "$lt": end}})
    elif scheme_name== 'All':
        all_works_dict = Database.find("works", {
            "$and": [ {"end_date": {"$gte": start, "$lt": end}},
                     {"scheme_group_name": scheme_group_name}]})
    elif work_group_name == 'All':
        all_works_dict = Database.find("works", {
            "$and": [ {"end_date": {"$gte": start, "$lt": end}}, {"scheme_name":scheme_name},
                     {"scheme_group_name": scheme_group_name}]})
    elif work_type == 'All':
        all_works_dict = Database.find("works", {
            "$and": [{"end_date": {"$gte": start, "$lt": end}}, {"scheme_name": scheme_name},
                     {"work_group_name": work_group_name},
                     {"scheme_group_name": scheme_group_name}]})

    else:

        all_works_dict = Database.find("works", {"$and": [{"end_date": {"$gte": start, "$lt": end}}, {"scheme_name": scheme_name}, {"work_group_name":work_group_name}, {"work_type":work_type},

                                                        {"scheme_group_name": scheme_group_name}]})

    for tran in all_works_dict:

        all_works.append(tran)

    all_w = json.dumps(all_works, default=json_util.default)

    return all_w

@app.route('/rawschemegroupname')

def get_scheme_group_name():

    district_intents_array = []

    district_intents = Database.find("schemes", {})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawschemename/<string:scheme_group_name>')

def get_scheme_name(scheme_group_name):

    district_intents_array = []

    district_intents = Database.find("schemes", {"scheme_group_name" : scheme_group_name})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawworkgroupname/<string:scheme_group_name>/<string:scheme_name>')

def get_work_group_name(scheme_group_name, scheme_name):

    district_intents_array = []

    district_intents = Database.find("schemes", {"$and": [{"scheme_group_name": scheme_group_name},

                                                        {"scheme_name": scheme_name}]})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawworktype/<string:scheme_group_name>/<string:scheme_name>/<string:work_group_name>')

def get_work_type(scheme_group_name, scheme_name, work_group_name):

    district_intents_array = []

    district_intents = Database.find("schemes", {"$and": [{"scheme_group_name": scheme_group_name},

                                                          {"work_group_name" : work_group_name},

                                                          {"scheme_name": scheme_name}]})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawschemename')

def get_scheme_name_second():

    district_intents_array = []

    district_intents = Database.find("schemes", {})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawworkgroupname')

def get_work_group_name_second():

    district_intents_array = []

    district_intents = Database.find("schemes", {})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/rawworktype')

def get_work_type_second():

    district_intents_array = []

    district_intents = Database.find("schemes", {})

    for intent in district_intents:

        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/Deadline_violation_stages')

def Deadline_violation_stages():

    email = session['email']

    user = User.get_by_email(email)

    if email is not None:

              return render_template('deadline_violation_stages_sheet.html', user=user)

    else:

        return render_template('login_fail.html', user=user)


@app.route('/DeadlineViolationStagesReport')
def deadline_violation_stages_report():
    stage = []
    d = datetime.today() - timedelta(days=30)
    stage_dict = Database.find("stages",{"$and": [{"stage_status": "Open"}, {"start_date": {"$lte": d}}]})

    for tran in stage_dict:
        stage.append(tran)

    single_stage = json.dumps(stage, default=json_util.default)

    return single_stage


@app.route('/viewimagestage/<string:_id>', methods=['POST', 'GET'])
def preview_image(_id):
    URI = os.environ['MONGODB_URI']
    client = pymongo.MongoClient(Database.URI)
    DATABASE = client['heroku_thg5d5x0']

    email = session['email']

    user = User.get_by_email(email)

    # URI = "mongodb://127.0.0.1:27017"
    # client = pymongo.MongoClient(URI)
    # DATABASE = client['Dindugul']

    fid = ""
    fs = gridfs.GridFS(DATABASE)

    print(DATABASE['road_images'].find({'fileid': _id}))

    for output_data1 in DATABASE['road_images'].find({'stageid': _id}):
        fid = output_data1["fileid"]

    output_data = fs.get(fid).read()

    base64_data = codecs.encode(output_data, 'base64')
    image = base64_data.decode('utf-8')

    if user.designation == 'HQ Staff':
        return render_template('road_image_display.html', images=image, user=user)
    else:
        return render_template('road_image_display_blocks.html', images=image, user=user)


@app.route('/panchayats/<string:block>')
def get_panchayat_name(block):

    district_intents_array = []
    district_intents = Database.find("panchayats", {"Block Name": block})
    for intent in district_intents:
        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

@app.route('/deletework/<string:work_id>')

def deletework(work_id):

        email = session['email']

        user = User.get_by_email(email)

        Work.deletefrom_mongo(work_id= work_id)

        return render_template('deleted.html', user=user)

@app.route('/deletestage/<string:_id>')

def deletestage(_id):

        email = session['email']

        user = User.get_by_email(email)

        Stage.deletefrom_mongo(_id= _id)

        return render_template('deleted.html', user=user)

@app.route('/habitations/<string:block>/<string:panchayat>')
def get_habitation_name(block, panchayat):

    district_intents_array = []
    district_intents = Database.find("panchayats", {"$and": [{"Block Name": block},
                                                             {"Village Panchayats Name": panchayat}]})
    for intent in district_intents:
        district_intents_array.append(intent)

    completed_intents = json.dumps(district_intents_array, default=json_util.default)

    return completed_intents

# @app.before_request

# def limit_remote_addr():

#     if request.headers.getlist("X-Forwarded-For")[0] == '106.208.39.7':

#         return abort(403)  # Forbidden

if __name__ == '__main__':
    app.run(port=4065, debug=True)

