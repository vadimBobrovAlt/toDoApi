from playhouse.shortcuts import model_to_dict

from models.main import Task


class TaskClass:

    def get_tasks(self, user_id, is_done=False):
        tasks = Task.select(Task.id, Task.title, Task.description, Task.is_done).where(Task.user_id == user_id)
        print(tasks)
        if is_done == False:
            tasks = tasks.where(Task.is_done == False)
        return [model_to_dict(item) for item in tasks]

    def get_task(self, task_id, user_id):
        task = Task.get_or_none(Task.id == task_id, Task.user_id == user_id)
        if task is not None:
            task = model_to_dict(task)
            return {'id': task['id'], "title": task['title'], 'description': task['description'], 'is_done': task['is_done']}
        else:
            return None

    def create_task(self, data, user_id):
        task = Task.create(title=data['title'], description=data['description'], user_id=user_id)
        return {"id": task.id, "title": task.title, "description": task.description}

    def update_task(self, task_id, data):
        q = Task.update(data).where(Task.id == task_id)
        if q.execute() > 0:
            return "Задача успешно обновлена"
        else:
            return "При обновлении задачи возникла ошибка"

    def delete_task(self, task_id, user_id):
        q = Task.delete().where(Task.id == task_id).where(Task.user_id == user_id)
        if q.execute() > 0:
            return "Задача успешно удалена"
        else:
            return "При удалении задачи возникла ошибка"
