from app import db 
from .user import User
from .profile import Profile
from .message import Message
from .event import Event
# Just after db.init_app(app)
from app import models

from .. import db 
