from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from states.states_groups import ABP
from aiogram.fsm.context import FSMContext

from states.manage_states import stop_fsm


states_router = Router()


@states_router.message(ABP.fcs)
async def handle_fcs(message: Message, state: FSMContext):

    if len(message.text.split()) != 3:
        await message.answer("ФИО должно быть в формате `Фамилия Имя Отчество!`")
        return

    await state.update_data({"fcs": message.text})
    await state.set_state(ABP.city)
    await message.answer("""
В каком городе или населённом пункте ты живёшь? 
    """)


@states_router.message(ABP.city)
async def handle_city(message: Message, state: FSMContext):
    await state.update_data({"city": message.text})
    await state.set_state(ABP.school)
    await message.answer("""
Ого, всегда мечтал там побывать!🤩
Кстати, а где ты учишься? Скажи название своей школы:
    """)


@states_router.message(ABP.school)
async def handle_school(message: Message, state: FSMContext, bot: Bot):
    await state.update_data({"school": message.text})
    await state.set_state(None)

    await message.answer("""
    Спасибо огромное, рад был познакомиться❤️
Твою заявку рассмотрят в течении дня, и одобрят заявку на вступление! 🤩
    """, reply_markup=ReplyKeyboardRemove())
    await stop_fsm(message, state, bot)
    # await message.answer(
    #     "Для добавления тебя в контакты отправь свой номер телефона. Нажми на кнопку для того чтобы это сделать",
    #     reply_markup=kb
    # )


# @states_router.message(ABP.phone)
# async def handle_phone(message: Message, state: FSMContext, bot: Bot):
#     if message.contact.user_id != message.from_user.id:
#         await message.answer("Нужно отправить *ваш* номер через кнопку.", parse_mode="Markdown")
#         return
#
#     phone = message.contact.phone_number
#     await state.update_data(phone=phone)
#     await message.answer("Спасибо! Номер получен. Вы записаны в базу данных! Ожидайте принятия запроса на вступление в чат.", reply_markup=ReplyKeyboardRemove())
#     await stop_fsm(message, state, bot)

