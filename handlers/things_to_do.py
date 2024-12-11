from aiogram import Router, types, F
from aiogram.filters import StateFilter
from keybords.for_navigate import homework_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value

TASKS = []

work_router = Router()


@work_router.message((F.text == 'виберiть опцiю'))
async def works_cmd(message: types.Message):
    await message.answer('Виберiть що хочете зробити:',
                         reply_markup=homework_keyboard)


@work_router.message((F.text == 'список завдань'))
async def add_work(message: types.Message):
    if not TASKS:
        await message.answer("немає завдань")
        return
    for i in range(len(TASKS)):
        text = as_marked_section(
            Underline(Bold(f'Завдання {i+1}')),
            as_key_value('Задача', TASKS[i]['topic']),
            as_key_value('Важливiсть', TASKS[i]['number']),
            as_key_value('Тема', TASKS[i]['content']),
            marker='📌 '
        )
        await message.answer(text.as_html())


class AddHomework(StatesGroup):
    topic = State()
    number = State()
    content = State()


@work_router.message(StateFilter(None), (F.text == 'додати задачу'))
async def add_work(message: types.Message, state: FSMContext):
    await message.answer('введiть завдання:',
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddHomework.topic)


@work_router.message(AddHomework.topic, F.text)
async def add_topic(message: types.Message, state: FSMContext):
    content = message.text.lower()
    await state.update_data(topic=content)
    await message.answer('введiть важливiсть завдання вiд 1 до 5 де 5 дуже важливо а 1 можно зробити в останню чергу: ')
    await state.set_state(AddHomework.number)


@work_router.message(AddHomework.number, F.text)
async def add_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer('введiть тему: ')
    await state.set_state(AddHomework.content)


@work_router.message(AddHomework.content, F.text)
async def add_content(message: types.Message, state: FSMContext):
    content = message.text.lower()
    await state.update_data(content=content)
    await message.answer('завдання успiшно було додано',
                         reply_markup=homework_keyboard)
    data = await state.get_data()
    await message.answer(str(data))
    TASKS.append(data)
    await state.clear()


@work_router.message((F.text == 'видалити завдання'))
async def delete_work(message: types.Message, state: FSMContext):
    if not TASKS:
        await message.answer("немає завдань для видалення.")
        return
    tasks_text = 'ось список завдань:\n'
    for task in TASKS:
        tasks_text += f'{task["topic"]}\n'

    await message.answer(f'{tasks_text}\nвведіть назву завдання, яке бажаєте видалити:')
    await state.set_state('delete_task')

@work_router.message(lambda message, state: True)
async def delete_task(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'delete_task':
        task_name = message.text.lower()
        global TASKS
        for task in TASKS:
            if task['topic'].lower() == task_name:
                TASKS.remove(task)
                await message.answer(f'Завдання "{task_name}" видалено.')
                await state.clear()
                return
        await message.answer(f'Завдання "{task_name}" не знайдено.')
        await state.clear()

# class EditHomework(StatesGroup):
#     select = State()
#     choose = State()
#     edit = State()
#
#
# @homework_router.message((F.text.lower() == 'поредагувати завдання'))
# async def edit_task(message: types.Message, state: FSMContext):
#     if not TASKS:
#         await message.answer("немає завдань для редагування.")
#         return
#
#     tasks = "ось список завдань:\n"
#     for i, task in enumerate(TASKS, 1):
#         tasks += f"{i}. {task['topic']}\n"
#
#     await message.answer(f"{tasks}\nвведіть номер завдання, яке бажаєте редагувати:")
#     await state.set_state(EditHomework.select)
#
#
# @homework_router.message(EditHomework.select)
# async def select_task(message: types.Message, state: FSMContext):
#     try:
#         task_index = int(message.text.strip()) - 1
#         if 0 <= task_index < len(TASKS):
#             await state.update_data(task_index=task_index)
#             await message.answer(
#                 "що ви хочете редагувати?\n"
#                 "1. назва\n"
#                 "2. тема\n"
#                 "3. задача\n"
#                 "введіть номер:"
#             )
#             await state.set_state(EditHomework.choose)
#         else:
#             await message.answer("невірний номер завдання. Спробуйте ще раз.")
#     except ValueError:
#         await message.answer("будь ласка, введіть номер завдання.")
#
#
# @homework_router.message(EditHomework.choose)
# async def choose_field(message: types.Message, state: FSMContext):
#     field = {
#         "1": "topic",
#         "2": "number",
#         "3": "content",
#     }
#     choice = message.text.strip()
#     if choice in field:
#         await state.update_data(field=field[choice])
#         field_name = {
#             "topic": "назву",
#             "number": "важливість",
#             "content": "тему",
#         }[field[choice]]
#         await message.answer(f"введіть нову {field_name}:")
#         await state.set_state(EditHomework.edit)
#     else:
#         await message.answer("невірний вибір")
#
#
# @homework_router.message(EditHomework.edit)
# async def edit_field(message: types.Message, state: FSMContext):
#     new_value = message.text.lower()
#     data = await state.get_data()
#     task_index = data.get("task_index")
#     field = data.get("field")
#
#     if task_index is not None and field:
#         TASKS[task_index][field] = new_value
#         await message.answer("зміни успішно збережено")
#         await state.clear()
#     else:
#         await message.answer("сталася помилка спробуйте ще раз")
#         await state.clear()