from aiogram import types, Dispatcher
from db import adminDB,shopDB, UserDB
import markups as nav
from create_bot import dp, bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from States import ProductState, UserState, Userhey,sendingState,disableALLCat
from filters import IsAdmin


user_db = UserDB.UserDB('database.db')
AdminShop = adminDB.AdminShopDB('database.db')


async def start(message: types.Message):
    if(not user_db.user_exists(message.from_user.id)):
        user_db.add_user(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup = nav.MainKeyboard())

async def deleteById(msg: types.Message):
    
    await msg.bot.send_message(msg.from_user.id, 'Введите ID товара для удаления из каталога')
    await UserState.name.set()

async def delete(msg: types.Message, state: FSMContext):
    msg.text = int(msg.text)
    AdminShop.delete_id(msg.text)
    #await UserState.next()
    await state.finish() # либо же UserState.address.set()

#Восстановлние товара в каталоге
class RestoreProduct:

    async def restoreById(msg: types.Message):
        
        await msg.bot.send_message(msg.from_user.id, 'Введите ID товара для восстоновления в каталог')
        await Userhey.usrname.set()

    async def restore(msg: types.Message, state: FSMContext):
        msg.text = int(msg.text)
        AdminShop.restore_id(msg.text)
        #await UserState.next()
        await state.finish()
Restore_Product = RestoreProduct()


#Отключение категории товара
class DisableCategories:

    async def disableAllCategories(msg: types.Message):
        
        await msg.bot.send_message(msg.from_user.id, 'Введите название категории которую вы хотите отключить из поиска')
        await disableALLCat.step1.set()

    async def disableAllCategories2(msg: types.Message, state: FSMContext):
        AdminShop.disable_all_categories(msg.text)
        await msg.bot.send_message(msg.from_user.id, 'Категория отключена!')
        await state.finish()
Disable_Categories = DisableCategories()


#Рассылка сообщения всем пользователям
class SendAllUsers:
    def __init__(self):
        self.newsletter = ""

    async def sendMessageAllUser(self, msg: types.Message):
        await msg.bot.send_message(msg.from_user.id, 'Напишите сообщнение которое будет отправленно всем пользователям')
        await sendingState.awaitMsg.set()

    async def sendMessageAllUser_1(self, msg: types.Message, state: FSMContext):
        self.newsletter = msg.text
        await msg.bot.send_message(msg.from_user.id, f"*Помните что это сообщнение увидят все пользователи бота! Перечитайте его ещё раз внимательно и проверьте всю информацию*\n\n {self.newsletter}",
                                    parse_mode="markdown")
        await msg.bot.send_message(msg.from_user.id, "Что бы отправить сообщние напишите в  чат \"отправитьвсем\" ") 
        await sendingState.confirmation.set()

    async def sendMessageAllUser_2(self, msg: types.Message, state: FSMContext):
        if msg.text == "отправитьвсем":
            allUser = user_db.get_all_user_id()
            i = 0
            for item in allUser:
                await msg.bot.send_message((allUser[i][0]), self.newsletter)
                i = i + 1
            await state.finish()
            # await sendingState.photo.set()
Send_All_Users = SendAllUsers()


#Добавение нового товара в каталог
class AddNewProduct:
    def __init__(self):
        self.product = []

    async def start(self, msg: types.Message):
        
        await msg.bot.send_message(msg.from_user.id, 'Введите категорию товара')
        await ProductState.categories.set()

    async def process_step(self, msg: types.Message, state: FSMContext, next_state: State, message_text: str):
        self.product.append(msg.text)
        await msg.bot.send_message(msg.from_user.id, message_text)
        await next_state.set()

    async def categories(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.collection, 'Введите коллекцию товара')

    async def collection(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.name, 'Введите имя товара')

    async def name(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.photo, 'Введите фото товара')

    @dp.message_handler(content_types=types.ContentType.PHOTO, state=ProductState.photo)
    async def photo(message: types.Message, state: FSMContext):
        # Получаем список фотографий в сообщении
        photo_info = message.photo[-1]
        # Скачиваем изображение
        photo_data = await photo_info.download()
        # Преобразуйте изображение в байты
        with open(photo_data.name, 'rb') as image_file:
            image_bytes = image_file.read()
        # Добавляем данные изображения в список products
        Add_New_Product.product.append(image_bytes)
        
        # Переход к следующему состоянию
        await message.bot.send_message(message.from_user.id, 'Введите описание товара')
        await ProductState.description.set()

    async def description(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.color, 'Введите цвет товара')

    async def color(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.price, 'Введите цену товара')

    async def price(self, msg: types.Message, state: FSMContext):
        await self.process_step(msg, state, ProductState.prin, 'Все данные получены')

    async def printProduct(self, msg: types.Message, state: FSMContext):
        await msg.bot.send_message(msg.from_user.id, 'Готово')
        AdminShop.add_new_product(self.product[0], self.product[1], self.product[2],self.product[3], self.product[4], self.product[5], self.product[6])
        self.product = []
        await state.finish()
Add_New_Product = AddNewProduct() 

def register_handler_admin(dp : Dispatcher):
    dp.register_message_handler(start, commands="start")
    
    dp.register_message_handler(deleteById, IsAdmin(), commands="delete_id")
    dp.register_message_handler(delete, state=UserState.name)

    dp.register_message_handler(Restore_Product.restoreById,IsAdmin(), commands="restore_id")
    dp.register_message_handler(Restore_Product.restore, state=Userhey.usrname)

    dp.register_message_handler(Add_New_Product.start,IsAdmin(), commands="AddNewProduct")
    dp.register_message_handler(Add_New_Product.categories, state=ProductState.categories)
    dp.register_message_handler(Add_New_Product.collection, state=ProductState.collection)
    dp.register_message_handler(Add_New_Product.name, state=ProductState.name)
    dp.register_message_handler(Add_New_Product.description, state=ProductState.description)
    dp.register_message_handler(Add_New_Product.color, state=ProductState.color)
    dp.register_message_handler(Add_New_Product.price, state=ProductState.price)
    dp.register_message_handler(Add_New_Product.printProduct, state=ProductState.prin)

    dp.register_message_handler(Send_All_Users.sendMessageAllUser,IsAdmin(), commands="SendAll")
    dp.register_message_handler(Send_All_Users.sendMessageAllUser_1, state=sendingState.awaitMsg)
    dp.register_message_handler(Send_All_Users.sendMessageAllUser_2, state=sendingState.confirmation)

    dp.register_message_handler(Disable_Categories.disableAllCategories,IsAdmin(), commands="disableAllCategories")
    dp.register_message_handler(Disable_Categories.disableAllCategories2, state=disableALLCat.step1)