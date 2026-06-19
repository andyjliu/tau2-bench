from tau2.domains.mock.data_model import MockDB, Task, TaskStatus, User
from tau2.domains.taskdesk.utils import TASKDESK_DB_PATH

# TaskDesk reuses the mock data model (users + tasks). It is intentionally a
# thin extension: the schema is identical to the mock domain, and the added
# behavior lives entirely in the toolkit (delete / reassign).

__all__ = ["TaskDeskDB", "Task", "TaskStatus", "User", "get_db"]


class TaskDeskDB(MockDB):
    """Task help-desk database. Same schema as MockDB (users + tasks)."""


def get_db():
    return TaskDeskDB.load(TASKDESK_DB_PATH)
