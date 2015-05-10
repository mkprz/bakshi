from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UnicodeText,
    DateTime
)
import datetime
import clips
import os
import logging
log = logging.getLogger(__name__)

# Router config modules
import qos
import guestwifi

class KnowledgeBaseError(StandardError):
    pass


from sqlalchemy.ext.declarative import (
    declarative_base,
    # DeclarativeMeta
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    # reconstructor
)

# http://docs.pylonsproject.org/projects/pyramid-cookbook/en/latest/pylons/models.html#transaction-manger
#
# A transaction manager takes care of the commit-rollback cycle for you.
# The database session in both applications above is a scoped session, meaning it is
# a threadlocal global and must be cleared out at the end of every request.
# A transaction manager takes this a step further by committing any changes made
# during the request, or if an exception was raised during the request, it rolls back the changes.
# The ZopeTransactionExtension provides a module-level API in case the view wants
# to customize when/whether committing occurs.
# The upshot is that your view method does not have to call DBSession.commit():
# the transaction manager will do it for you. Also, it does not have to put the
# changes in a try-except block because the transaction manager will call DBSession.rollback()
# if an exception occurs.
#
# A side effect is that you cannot call DBSession.commit()
# or DBSession.rollback() directly. If you want to precisely control when something
# is committed, you will have to do it this way:
#   import transaction
#
#   transaction.commit()
# # Or:
#   transaction.rollback()

from zope.sqlalchemy import ZopeTransactionExtension
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


# from inflection import tableize
# class MyMeta(DeclarativeMeta):
#     def __init__(cls, clsname, parents, dct):
#         dct['__tablename__'] = tableize(clsname)
#         dct["id"] = Column(Integer, primary_key=True)
#         dct["created_at"] = Column(DateTime, default=datetime.datetime.utcnow)
#         dct["updated_at"] = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#
# MyBase = declarative_base(metaclass=MyMeta)
Base = declarative_base()


# database should capture responses to questions per interview
# save responses in sequence
# and re-run the responses in order to assert facts
# and continue with interview or result in finished uci script
#

import urllib
import urllib2


# utility functions to be called from within CLIPS
def setprompt(clips_goalname, *clips_choices):
    def directly(goalname, choices):
        i = Interview.setprompt(goalname, ",".join(choices))
        log.debug("clips python-call setprompt: %s, %s", i.prompt_text, i.csv_choices)

    def indirectly(goalname, choices):
        # so that CLIPS callbacks can create/modify database mapped objects
        # without cluttering the code with transaction code, lets make web calls
        # instead of direct calls. This way the pyramid_tm module can do its thing.
        data = {
            "goalname": goalname,
            "choices": ",".join(choices)}
        request_data = urllib.urlencode(data)
        log.debug("clips python-call setprompt*WEB*: %s", request_data)
        try:
            response = urllib2.urlopen("http://localhost:6543/kbhook/setprompt", request_data)
            response_data = response.read()
        except urllib2.HTTPError, instance:
            log.debug(instance.msg)
            return clips.Symbol("error")
        data = response_data.split('\n')

    goalname = str(clips_goalname)
    choices = [str(c) for c in clips_choices]
    directly(goalname, choices)
    # indirectly(goalname, choices)
    return clips.Symbol("ok")

def getprompt(clips_goalname):
    i = Interview.get_current()
    return clips.Symbol( i.selected_choice )

def addnetcfg(module_name, cfg_name):
    try:
        i = Interview.get_current()
        # call function with name cfg_name from module with name module_name

        log.debug("=====================calling function: %s::%s()", module_name, cfg_name)
        literally_a_module = eval(str(module_name))
        log.debug("=====================module: %s", str(literally_a_module))
        config_func = getattr(literally_a_module, cfg_name)
        log.debug("=====================function: %s", str(config_func))
        config_text = config_func()
        log.debug("=====================result: '%s'", config_text)
        i.config_text = config_text
        DBSession.add(i)
    except:
        return clips.Symbol("ERROR")
    log.debug("exiting addnetcfg")
    return clips.Symbol("ok")


# interviews (id, created_at, updated_at, apply_at, undo_at)
# responses (id, interview_id, node_name, question, selected_choice, [branches], [netcfg], created_at, updated_at)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), default=u'', nullable=False)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)
    last_access = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_from_ip = Column(Unicode, default=u'')
    updated_from_ip = Column(Unicode, default=u'')

    interviews = relationship("Interview", backref="user")


# class PromptState(Base):
#     __tablename__ = 'prompt_states'
#     id = Column(Integer, primary_key=True)
#     interview_id = Column(Integer, ForeignKey('interviews.id'), nullable=False)
#     # node = Column(Unicode(255), unique=True, nullable=False)
#     prompt_text = Column(UnicodeText, nullable=False)
#     csv_choices = Column(UnicodeText, default=u'', nullable=False)
#     selected_choice = Column(UnicodeText, default=u'', nullable=False)
#     watchtext = Column(UnicodeText, default=u'', nullable=False)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
#     created_from_ip = Column(Unicode, default=u'')
#     updated_from_ip = Column(Unicode, default=u'')
#
#     #belong_to Interview, Interview has_one prompt_state
#     interview = relationship("Interview", backref=backref("prompt_state", uselist=False))


class Interview(Base):
    __tablename__ = 'interviews'
    id = Column(Integer, primary_key=True)#, sqlite_autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_current = Column(Integer, nullable=False, default=0)
    prompt_text = Column(UnicodeText, default=u'', nullable=False)
    csv_choices = Column(UnicodeText, default=u'', nullable=False)
    selected_choice = Column(UnicodeText, default=u'', nullable=False)
    watchtext = Column(UnicodeText, default=u'', nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_from_ip = Column(Unicode, default=u'')
    updated_from_ip = Column(Unicode, default=u'')
    last_request_ip = Column(Unicode, default=u'')
    config_text = Column(UnicodeText, default=u'')

    default_filename = "erc_config.sh"

    @classmethod
    def setprompt(cls, goalname, choices_str):
        i = Interview.get_current()
        i.prompt_text = goalname + "?"
        i.csv_choices = choices_str
        i.selected_choice = ""
        return i

    @classmethod
    def find(cls, instance_id):
        return DBSession.query(Interview).filter(Interview.id == instance_id).first()

    @classmethod
    def get_current(cls):
        # get the earliest interview that is marked as current
        # new interviews might be created but until the earliest one is closed-out, they are not current
        i = DBSession.query(Interview).filter(Interview.is_current == 1).order_by(Interview.created_at).first()
        if( i is None ):
            log.debug("creating new Interview")
            i = Interview()
            i.user_id=1
            i.is_current=1
            DBSession.add(i)
        else:
            log.debug("reusing existing Interview")

        # i.prompt_text = ""
        # i.csv_choices = ""
        # i.selected_choice = ""
        # i.watchtext = ""
        return i

    @property
    def config(self):
        pass

    @classmethod
    def clear_and_reset(cls):
        try:
            clips.ClearPythonFunctions()
            clips.RegisterPythonFunction(setprompt)
            clips.RegisterPythonFunction(getprompt)
            clips.RegisterPythonFunction(addnetcfg)
            # cls.env = clips.Environment()
            clips.Clear()
            clips.DebugConfig.ExternalTraceback = True	# print traceback on error
            clips.DebugConfig.ActivationsWatched = True
            clips.DebugConfig.FactsWatched = True
            clips.DebugConfig.RulesWatched = True
            clips.DebugConfig.SlotsWatched = True
            clips.DebugConfig.DribbleOn(os.path.abspath("bakshi/static/pyclips.log"))
            # facts_file = os.path.abspath("bakshi/static/bc-winedemo.clp")
            engine_file = os.path.abspath("bakshi/static/inference-engine-bc.clp")
            clips.Load(engine_file)
            clips.Reset()
            clips.Eval("(focus BC)")
            # clips.Eval("(assert (goal (attribute best-color)))")
            # clips.BatchStar(facts_file)
        except clips.ClipsError:
            error_str = clips.ErrorStream.Read()
            error_str += "--------------------------\n\n"
            # error_str += clips.TraceStream.Read()
            print error_str
            raise KnowledgeBaseError(error_str)
        return

    @classmethod
    def open_and_start(cls, ip_address):
        try:
            i = Interview(ip_address)
            Interview.next()
        except clips.ClipsError:
            raise KnowledgeBaseError(clips.ErrorStream.Read())
        return i

    @classmethod
    def next(cls):
        try:
            # step through rules until either no more rules or a new prompt is set
            # while True:
            rules_fired = clips.Run()
            log.debug("rules_fired: %s", rules_fired)
            watchtext = ""

            # watchtext += "Agenda\n========\n" + '\n'.join(map(str, clips.RuleList()))
            # watchtext += "\n\nFacts\n========\n" + '\n'.join(map(str, clips.FactList()))

            if( clips.FactListChanged() ):
                watchtext += "\n\nFactListChanged"
            if( clips.AgendaChanged() ):
                watchtext += "\n\nAgendaChanged"
            clips_trace = clips.TraceStream.Read()
            if( not clips_trace is None ):
                watchtext += "\n\nTrace\n========\n" + clips_trace

            i = Interview.get_current()
            i.watchtext = watchtext

        except clips.ClipsError:
            raise KnowledgeBaseError(clips.ErrorStream.Read())
        return rules_fired

    @classmethod
    def close(cls):
        try:
            clips.ClearPythonFunctions()
            clips.Clear()
            clips.Reset()
        except clips.ClipsError:
            raise KnowledgeBaseError(clips.ErrorStream.Read())
        i = Interview.get_current()
        i.is_current = 0

    def build_config(self, request):
        with open(self.default_filename, 'a') as myfile:
            myfile.writelines(self.config_text)

    def append_configuration(self, config_lines):
        self.config_text += config_lines
