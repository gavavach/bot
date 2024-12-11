from aiogram import types

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='виберiть опцiю')
        ],
        [
          types.KeyboardButton(text='видалити завдання')
        ],
        [
            types.KeyboardButton(text='про бота')
        ],
        [

          types.KeyboardButton(text='поредагувати завдання')
        ]


    ],
    resize_keyboard=True,
    input_field_placeholder='All commands'
)


homework_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='додати задачу')
        ],
        [
            types.KeyboardButton(text='список завдань')
        ],
        [
            types.KeyboardButton(text='видалити завдання')
        ]
        # [
        #   types.KeyboardButton(text='поредагувати завдання')
        # ]

    ],
    resize_keyboard=True,
    input_field_placeholder='Homework commands'
)
buttons_lst = ['qwe', 'asd', 'zxc']
test_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text=i)
        ] for i in buttons_lst
    ],
    resize_keyboard=True,
    input_field_placeholder='Homework commands'
)