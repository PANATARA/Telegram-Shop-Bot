import io
from aiogram import types, Dispatcher
from db import shopDB, UserDB
import markups as nav
from create_bot import bot


user_db = UserDB.UserDB('database.db')
ClientShop = shopDB.ClientShopDB('database.db')

class Client:
    def __init__(self):
        self.bagNum = 0
        self.num = '1/3'


    async def main_hand(self, msg: types.Message):

        if msg.text == 'Мои Избранные':
            favorites = ClientShop.get_my_wish_list(msg.from_user.id, "favorites")
            if favorites:
                i = 0
                for item in favorites:
                    cards = ClientShop.get_card(productID = favorites[i])
                    text = cards[0]
                    photos = cards[1]
                    await msg.bot.send_photo(msg.from_user.id, photo = photos[0][0],
                                               caption = f"*{text[0][1][0]}*\n\n{text[0][2][0]}\n\n Цена: *{text[0][3][0]}*₽\n\n ID товара: {text[0][0][0]}",
                                               reply_markup=nav.INKB_FAV(), 
                                               parse_mode="markdown")
                    i = i + 1
            else:
                await msg.bot.send_message(msg.from_user.id, "Вы ещё не добавили ни одного товара:(")


        elif msg.text == 'Главное меню':

            await msg.bot.send_message(msg.from_user.id,'Главное меню', reply_markup = nav.MainKeyboard())

        elif msg.text == 'Каталог':

            await msg.bot.send_message(msg.from_user.id,'Вот наш актуальный каталог:', reply_markup = nav.makeInlineKeyboard()[0])


        elif msg.text == 'Корзина':

            self.bagNum = 0
            cards = self.getTextPhoto(msg.from_user.id)

            if cards:
                text = cards[0]
                photos = cards[1]
                
                await msg.bot.send_photo(msg.from_user.id, photo = photos[0][0],
                                        caption = f"*{text[0][1][0]}*\n\n{text[0][2][0]}\n\n Цена: *{text[0][3][0]}*₽\n\n ID товара: {text[0][0][0]}",
                                        reply_markup=nav.INKB_BAG(self.num, ClientShop.get_price(userID=msg.from_user.id),
                                                                  quantity= ClientShop.update_quantity(int(text[0][0][0]), msg.from_user.id, None)), 
                                        parse_mode="markdown")
            else:
                await msg.bot.send_message(msg.from_user.id, "Корзина пуста:(")

        elif msg.text == 'Заказы':
            ClientShop.get_price(userID=msg.from_user.id)      

    async def nextCard(self, callback_query: types.CallbackQuery, list_type: int):
        self.bagNum += list_type
        cards = self.getTextPhoto(callback_query.message.chat.id)

        if cards:

            text = cards[0]
            photos = cards[1]
            file = types.InputMedia(media= types.InputFile(io.BytesIO(photos[0][0])), 
                                    caption=f"*{text[0][1][0]}*\n\n{text[0][2][0]}\n\n Цена: *{text[0][3][0]}*₽\n\n ID товара: {text[0][0][0]}",                                             
                                   parse_mode="markdown")
            
            await bot.edit_message_media(media = file, chat_id = callback_query.message.chat.id, message_id =  callback_query.message.message_id,
                    reply_markup=nav.INKB_BAG(self.num, ClientShop.get_price(userID=callback_query.from_user.id),
                                              quantity= ClientShop.update_quantity(int(text[0][0][0]), callback_query.from_user.id, None) ))


    async def addTolist(self, callback_query: types.CallbackQuery): # Добавлние в корзину или избранное
        check = ClientShop.add_product_to_wish_list(int(callback_query.message.caption[-1]),callback_query.from_user.id, callback_query.data)
        if check == "Товар добавлен в корзину" or check == "Товар уже у вас в корзине":
            await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, 
                                                reply_markup = nav.INKB_BAG(self.num, 
                                                                             ClientShop.get_price(userID=callback_query.from_user.id) ))
        await bot.answer_callback_query(callback_query.id, check)


    async def delete_item(self, callback_query: types.CallbackQuery, list_type: str): #Удаление из корзины или избранных

        name = ClientShop.delete_product_from_wish_list(int(callback_query.message.caption[-1]), 
                                                 callback_query.from_user.id, list_type)
        
        await bot.answer_callback_query(callback_query.id, f"Товар удалён из {name}")
        await self.nextCard(callback_query, 1)


    async def show_products(self, callback_query: types.CallbackQuery):#Показ каталога товаров

        card = ClientShop.get_card(cat = callback_query.data)
        rows = card[0]
        photorows = card[1]
        i = 0
        print(rows)
        for row in rows:

            await callback_query.message.answer_photo(photo = photorows[i][0],
                                       caption = f"*{rows[i][1][0]}*\n\n{rows[i][2][0]}\n\n Цена: *{rows[i][3][0]}*₽\n\n ID товара: {rows[i][0][0]}",
                                       reply_markup=nav.INKB_CARD(), 
                                       parse_mode="markdown")
            i = i + 1


    async def change_quanity(self, callback_query: types.CallbackQuery, list_type: int):

        result = ClientShop.update_quantity(int(callback_query.message.caption[-1]), callback_query.from_user.id, list_type )
        
        await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                        callback_query.message.message_id,
                                        reply_markup=nav.INKB_BAG(self.num, ClientShop.get_price(userID=callback_query.from_user.id),
                                                                   quantity=result))

    def getTextPhoto(self, chatid):
        bag = ClientShop.get_my_wish_list(chatid, "Bag")
        if self.bagNum == len(bag):
            self.bagNum = 0
        elif self.bagNum == -1:
            self.bagNum = len(bag) - 1
        self.num= "{}/{}".format(self.bagNum + 1, len(bag))
        if bag:
            cards = ClientShop.get_card(productID = bag[self.bagNum])
            return cards

client = Client()
def register_handler_client(dp : Dispatcher): 
    dp.register_message_handler(client.main_hand)
    dp.register_callback_query_handler(lambda cbq: client.delete_item(cbq, "favorites"), text="delete_from_favorites")
    dp.register_callback_query_handler(lambda cbq: client.delete_item(cbq, "Bag"), text="deleteFromBag")

    dp.register_callback_query_handler(client.addTolist, text = "favorites")
    dp.register_callback_query_handler(client.addTolist, text = "Bag")

    dp.register_callback_query_handler(lambda cbq: client.nextCard(cbq, 1), text = "next")
    dp.register_callback_query_handler(lambda cbq: client.nextCard(cbq, -1), text = "previous")


    dp.register_callback_query_handler(lambda cbq: client.change_quanity(cbq, 1), text = "plus")
    dp.register_callback_query_handler(lambda cbq: client.change_quanity(cbq, -1), text = "minus")

    categories_list = ClientShop.get_all_categories()
    for category in categories_list: 
        dp.register_callback_query_handler(client.show_products, text = category)