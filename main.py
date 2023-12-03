from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin

admin.register_handler_admin(dp)
client.register_handler_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
