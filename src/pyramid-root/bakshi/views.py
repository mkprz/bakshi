from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from models import (
    DBSession,
    User,
    Interview,
    # PromptState,
    KnowledgeBaseError
    )

import datetime
import os
import logging
log = logging.getLogger(__name__)

# config.add_route('home', '/')
@view_config(route_name='home', renderer='templates/home.mako')
def home(request):
    return {'ok': 200,}

# config.add_route('wizconfig', '/wizconfig')
@view_config(route_name='wizconfig', renderer='templates/wizconfig.mako')
def wizconfig(request):
    return {'ok': 200, 'test_path': os.path.abspath("test")}

# config.add_route('wizconfig', '/wizconfig/start/{id}')
@view_config(route_name='wizconfig_start', renderer='templates/wizconfig_prompt.mako')
def new_interview(request):
    ip_address = request.remote_addr
    try:
        Interview.clear_and_reset()
        rules_fired = Interview.next()
    except KnowledgeBaseError, instance:
        return Response(instance.args[0], content_type='text/plain', status_int=500)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'interview': Interview.get_current()}

# config.add_route('kbhook_setprompt', '/kbhook/setprompt')
# @view_config(route_name='kbhook_setprompt', renderer='templates/kbhook_setprompt.mako')
# def kbhook_setprompt(request):
#     ip_address = request.remote_addr
#     try:
#         goalname = request.params["goalname"]
#         choices_str = request.params["choices"]
#         log.debug("kbhook setting prompt")
#         i = Interview.setprompt(goalname, choices_str)
#         log.debug("kbhook comitting prompt")
#         # DBSession.add(prompt_state)
#     except KnowledgeBaseError, instance:
#         return Response(instance.args[0], content_type='text/plain', status_int=500)
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'interview': i}

# config.add_route('wizconfig_next', '/wizconfig/next/{id}')
@view_config(route_name='wizconfig_next', renderer='templates/wizconfig_prompt.mako')
def next(request):
    try:
        interview = DBSession.query(Interview).filter(Interview.id == request.matchdict["id"]).first()
        interview.selected_choice = request.params["selected_choice"]
        rules_fired = interview.next()
        DBSession.add(interview)

        # redirect
        # if( rules_fired == 0 ):
        #     raise HTTPFound(request.route_url("/wizconfig/review/" + str(interview.id)))

    except KnowledgeBaseError, instance:
        return Response(instance.args[0], content_type='text/plain', status_int=500)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'interview': interview, 'rules_fired': rules_fired}

# config.add_route('review', '/review/{id}')
@view_config(route_name='wizconfig_review', renderer='templates/wizconfig_review.mako')
def review(request):
    try:
        interview = DBSession.query(Interview).filter(Interview.id == request.params["id"]).first()
    except KnowledgeBaseError, instance:
        return Response(instance.args[0], content_type='text/plain', status_int=500)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'interview': interview}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_bakshi_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
