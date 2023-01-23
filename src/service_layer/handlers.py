import datetime
from typing import Callable, Dict, List, Type

from src.domain.commands.allocate_tasks import AllocateTasks
from src.domain.commands.command import Command
from src.domain.commands.create_task import CreateTask
from src.domain.commands.delete_task import DeleteTask
from src.domain.commands.edit_task import EditTask
from src.domain.commands.get_all_tasks import GetAllTasks
from src.domain.commands.get_main_task import GetMainTask
from src.domain.commands.get_tasks_by_type import GetTasksByType
from src.domain.commands.mark_task_as_done import MarkTaskAsDone
from src.domain.commands.mark_task_as_frozen import MarkTaskAsFrozen
from src.domain.commands.setup_tasks import SetupTasks
from src.domain.entities.complexity import Complexities
from src.domain.entities.status import Statuses
from src.domain.entities.task import DAY_END, DAY_START, Task, NO_PERIOD_VALUE
from src.domain.entities.task_type import TaskTypes
from src.domain.events.got_all_tasks import GotAllTasks
from src.domain.events.got_main_task import GotMainTask
from src.domain.events.task_is_created import TaskIsCreated
from src.domain.events.task_is_edited import TaskIsEdited
from src.domain.events.tasks_are_allocated import TasksAreAllocated
from src.service_layer.unit_of_work.abstract_unit_of_work import \
    AbstractUnitOfWork


async def get_all_tasks(
        cmd: GetAllTasks,
        uow: AbstractUnitOfWork,
):
    async with uow:
        tasks = await uow.repository.get_all_tasks()
    return GotAllTasks(tasks)


async def get_tasks_by_type(
        cmd: GetTasksByType,
        uow: AbstractUnitOfWork,
):
    async with uow:
        tasks = await uow.repository.get_tasks_by_type(cmd.status_title)
    return GotAllTasks(tasks)


async def get_actual_task(
        cmd: GetMainTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        main_task: Task = await uow.repository.get_actual_task(cmd.current_task_place)
    return GotMainTask(main_task)


async def create_task(
        cmd: CreateTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        new_item_id = await uow.repository.create_task(
            cmd.title, cmd.deadline, cmd.period,
            cmd.description, cmd.estimation,
            cmd.status_title, cmd.register_title,
            cmd.task_type_title,
        )
        await uow.commit()
    return TaskIsCreated(new_item_id)


async def edit_task(
        cmd: EditTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.edit_task(
            task_id=cmd.task_id,
            title=cmd.title,
            deadline=cmd.deadline,
            period=cmd.period,
            description=cmd.description,
            estimation=cmd.estimation,
            status_title=cmd.status_title,
            register_title=cmd.register_title,
            task_type_title=cmd.task_type_title,
            complexity_title=cmd.complexity_title,
        )
        await uow.commit()
    return TaskIsEdited(cmd.task_id)


async def delete_task(
        cmd: DeleteTask,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.delete_task(
            cmd.task_id
        )
        await uow.commit()


async def time_to_minutes(data: datetime.datetime):
    return data.minute + data.hour * 60


async def get_working_minutes_before_the_deadline(deadline: datetime.datetime, now=None):
    now = datetime.datetime.now() if not now else now
    now_time_to_minutes = await time_to_minutes(now)
    deadline_time_to_minutes = await time_to_minutes(deadline)
    day_start_time_to_minutes = await time_to_minutes(DAY_START)
    day_end_time_to_minutes = await time_to_minutes(DAY_END)
    remainder_days = (deadline - now).days
    remainder_minutes = 0
    # now minutes
    if day_start_time_to_minutes < now_time_to_minutes < day_end_time_to_minutes:
        remainder_minutes += now_time_to_minutes - day_start_time_to_minutes
    # last day minutes
    if day_start_time_to_minutes < deadline_time_to_minutes < day_end_time_to_minutes:
        remainder_minutes += deadline_time_to_minutes - day_start_time_to_minutes
    elif deadline_time_to_minutes > day_end_time_to_minutes:
        remainder_minutes += deadline_time_to_minutes - day_end_time_to_minutes
    total_minutes = remainder_minutes + remainder_days * 24 * 60
    return total_minutes


async def get_hottest_task_index(tasks: List[Task]) -> int:
    urgencies = [await get_urgency(task.deadline, task.estimation) for task in tasks]
    return urgencies.index(min(urgencies))


async def get_urgency(deadline: datetime.datetime, estimation: int, now=None):
    total_minutes = await get_working_minutes_before_the_deadline(deadline, now)
    urgency = total_minutes - estimation
    return urgency


async def define_complexity(urgency):
    if urgency < 0:
        return Complexities.IMPOSSIBLE.value
    elif urgency == 0:
        return Complexities.CRITICAL.value
    elif urgency < 1440:
        return Complexities.HARD.value
    elif urgency < 1440 * 7:
        return Complexities.MEDIUM.value
    else:
        return Complexities.EASY.value


async def allocate_tasks(
        cmd: AllocateTasks,
        uow: AbstractUnitOfWork,
):
    async with uow:
        all_tasks = await uow.repository.get_all_tasks()
    # get suitable tasks
    suitable_tasks = [
        task for task in all_tasks
        if task.task_type_title not in [
            TaskTypes.NEGATIVE.value,
            TaskTypes.NEGATIVE_WITH_PERIOD.value,
        ] and task.status_title == Statuses.IN_PROGRESS.value
    ]
    # allocate places between them
    place = 1
    total_minutes_to_complete_tasks_before_cur = 0
    while suitable_tasks:
        the_hottest_one_index = await get_hottest_task_index(suitable_tasks)
        the_hottest_one = suitable_tasks.pop(the_hottest_one_index)
        urgency = await get_urgency(
            the_hottest_one.deadline,
            total_minutes_to_complete_tasks_before_cur + the_hottest_one.estimation,
        )
        complexity_title = await define_complexity(urgency)
        async with uow:
            await uow.repository.change_place_and_complexity(
                task_id=the_hottest_one.item_id,
                place=place,
                complexity_title=complexity_title,
            )
            await uow.commit()
        place += 1
        total_minutes_to_complete_tasks_before_cur += the_hottest_one.estimation
    # for other set places to None and set complexities to UNDEFINED
    unsuitable_tasks = [
        task for task in all_tasks
        if not (task.task_type_title not in [
            TaskTypes.NEGATIVE.value,
            TaskTypes.NEGATIVE_WITH_PERIOD.value,
        ] and task.status_title == Statuses.IN_PROGRESS.value)
    ]
    for task in unsuitable_tasks:
        async with uow:
            await uow.repository.change_place_and_complexity(
                task_id=task.item_id,
                place=None,
                complexity_title=Complexities.UNDEFINED.value,
            )
            await uow.commit()
    return TasksAreAllocated()


async def mark_task_as_done(
        cmd: MarkTaskAsDone,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.change_task_status(
            cmd.task_id,
            Statuses.DONE.value,
        )
        await uow.commit()


async def mark_task_as_frozen(
        cmd: MarkTaskAsFrozen,
        uow: AbstractUnitOfWork,
):
    async with uow:
        await uow.repository.change_task_status(
            cmd.task_id,
            Statuses.FROZEN.value,
        )
        await uow.commit()


async def setup_tasks(
        cmd: SetupTasks,
        uow: AbstractUnitOfWork,
):
    # get all the tasks
    async with uow:
        tasks = await uow.repository.get_all_tasks()

    old_tasks = [
        task for task in tasks
        if task.deadline < datetime.datetime.now() and task.status_title == Statuses.IN_PROGRESS.value
    ]
    for task in old_tasks:
        # delete it
        async with uow:
            await uow.repository.delete_task(
                task.item_id,
            )
            await uow.commit()
        # if there is a period let's create new one
        if task.period != NO_PERIOD_VALUE and task.task_type_title in [
            TaskTypes.NEGATIVE_WITH_PERIOD.value,
            TaskTypes.COMMON_WITH_PERIOD.value,
        ]:
            new_deadline = await calculate_next_deadline(
                task.deadline,
                task.period,
            )
            cmd_to_create = CreateTask(
                task_type_title=task.task_type_title,
                period=task.period,
                deadline=new_deadline,
                estimation=task.estimation,
                description=task.description,
                status_title=Statuses.IN_PROGRESS.value,
                register_title=task.register_title,
                title=task.title,
            )
            await create_task(cmd_to_create, uow)


async def calculate_next_deadline(
        deadline: datetime.datetime,
        period: int,
):
    while deadline <= datetime.datetime.now():
        deadline += datetime.timedelta(days=period)
    return deadline


COMMAND_HANDLERS = {
    CreateTask: create_task,
    GetAllTasks: get_all_tasks,
    GetTasksByType: get_tasks_by_type,
    AllocateTasks: allocate_tasks,
    EditTask: edit_task,
    DeleteTask: delete_task,
    GetMainTask: get_actual_task,
    MarkTaskAsFrozen: mark_task_as_frozen,
    MarkTaskAsDone: mark_task_as_done,
    SetupTasks: setup_tasks,
}  # type: Dict[Type[Command], Callable]
