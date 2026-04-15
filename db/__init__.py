from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.base import Base

from db.availability import Availability
from db.user import User
from db.subscription import Subscription
from db.answer import Answer
from db.session import Session
from db.session_participant import SessionParticipant, FlagReason
from db.match import Match
from db.question_family import QuestionFamily
from db.questions import Question
from db.tree_node import TreeNode
from db.node_weight import NodeWeight
from config import settings

__all__ = [
    "Base", 
    "Availability", 
    "User", 
    "Subscription", 
    "Answer", 
    "Session",
    "SessionParticipant",
    "FlagReason",
    "Match", 
    "QuestionFamily", 
    "Question", 
    "TreeNode", 
    "NodeWeight", 
    "AsyncSessionLocal"
]


engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,
    pool_timeout=settings.db_pool_timeout,
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
