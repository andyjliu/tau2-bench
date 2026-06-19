from tau2.domains.mock.tools import MockTools
from tau2.domains.taskdesk.data_model import Task, TaskDeskDB
from tau2.environment.toolkit import ToolType, is_tool


class TaskDeskTools(MockTools):
    """Task help-desk tools.

    Extends the mock toolkit (``create_task``, ``get_users``,
    ``update_task_status``, ``transfer_to_human_agents``) with the ability to
    list, delete, and reassign tasks.
    """

    db: TaskDeskDB

    def __init__(self, db: TaskDeskDB) -> None:
        super().__init__(db)

    @is_tool(ToolType.READ)
    def get_tasks_for_user(self, user_id: str) -> list[Task]:
        """
        Get all tasks owned by a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The list of tasks owned by the user.

        Raises:
            ValueError: If the user is not found.
        """
        if user_id not in self.db.users:
            raise ValueError(f"User {user_id} not found")
        return [self.db.tasks[tid] for tid in self.db.users[user_id].tasks]

    @is_tool(ToolType.WRITE)
    def delete_task(self, task_id: str) -> str:
        """
        Permanently delete a task. Per policy, only completed tasks may be deleted.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            A confirmation message.

        Raises:
            ValueError: If the task is not found.
        """
        if task_id not in self.db.tasks:
            raise ValueError(f"Task {task_id} not found")
        for user in self.db.users.values():
            if task_id in user.tasks:
                user.tasks.remove(task_id)
        del self.db.tasks[task_id]
        return f"Task {task_id} deleted"

    @is_tool(ToolType.WRITE)
    def reassign_task(self, task_id: str, to_user_id: str) -> Task:
        """
        Reassign a task to a different existing user.

        Args:
            task_id: The ID of the task to reassign.
            to_user_id: The ID of the user to assign the task to.

        Returns:
            The reassigned task.

        Raises:
            ValueError: If the task or the destination user is not found.
        """
        if task_id not in self.db.tasks:
            raise ValueError(f"Task {task_id} not found")
        if to_user_id not in self.db.users:
            raise ValueError(f"User {to_user_id} not found")
        for user in self.db.users.values():
            if task_id in user.tasks:
                user.tasks.remove(task_id)
        self.db.users[to_user_id].tasks.append(task_id)
        return self.db.tasks[task_id]
