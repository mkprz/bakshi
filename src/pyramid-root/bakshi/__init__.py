from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('itsaseekreet')

from models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.include('pyramid_tm')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('wizconfig', '/wizconfig')
    config.add_route('wizconfig_start', '/wizconfig/start')
    # config.add_route('kbhook_setprompt', '/kbhook/setprompt')
    config.add_route('wizconfig_next', '/wizconfig/next/{id}')
    config.add_route('wizconfig_prev', '/wizconfig/prev/{id}')
    config.add_route('wizconfig_exit', '/wizconfig/exit/{id}')
    config.add_route('wizconfig_review', '/wizconfig/review/{id}')
    config.add_route('wizconfig_apply', '/wizconfig/apply/{id}')
    config.scan()
    config.set_session_factory(my_session_factory)
    return config.make_wsgi_app()
