async def moved_product_answer(callback, data):
    try:
        # await message.answer(
        #     f"<strong>Данные предоставлены в справочных целях !!!</strong>{chr(10)}{chr(10)}"
        # )
        if len(data) == 1:
            await callback.message.edit_text(
                text=f"<strong>Данные предоставлены в справочных целях !!!</strong>{chr(10)}{chr(10)}"
                f"По данной заявке было перемещено на склад {chr(10)}"
                f"Товар : {data[0]['product']}{chr(10)}"
                f"Партия : {data[0]['party_sign']}{chr(10)}"
                f"Количество : {data[0]['qt_moved']}",
                reply_markup=None,
            )
        if len(data) > 1:
            text = []
            it = 0
            for val in range(0, len(data)):
                if it == 0:
                    text.append(
                        f"<strong>Данные предоставлены в справочных целях !!!</strong>{chr(10)}{chr(10)}"
                        f"По данной заявке было перемещено на склад {chr(10)}"
                        f"Товар : {data[val]['product']}{chr(10)}"
                        f"Партия : {data[val]['party_sign']}{chr(10)}"
                        f"Количество : {data[val]['qt_moved']}{chr(10)}{chr(10)}",
                    )
                    it += 1
                else:
                    text.append(
                        f"Товар : {data[val]['product']}{chr(10)}"
                        f"Партия : {data[val]['party_sign']}{chr(10)}"
                        f"Количество : {data[val]['qt_moved']}{chr(10)}{chr(10)}",
                    )
            await callback.message.edit_text(
                text="".join(text),
                reply_markup=None,
            )
    except:
        await callback.message.edit_text(text="Данные отсутствуют", reply_markup=None)
