def calculate_products_amount(
        product_type_id: int,
        material_type_id: int,
        material_amount: int,
        product_param1: float,
        product_param2: float,
        loss_percent: float = 0.0
) -> int:
    """
    Расчет количества продукции из заданного количества сырья

    :param product_type_id: ID типа продукции
    :param material_type_id: ID типа материала
    :param material_amount: количество сырья
    :param product_param1: первый параметр продукции
    :param product_param2: второй параметр продукции
    :param loss_percent: процент потерь сырья (0-100)
    :return: количество продукции или -1 при ошибке
    """
    try:
        # Проверка входных данных
        if (product_type_id <= 0 or material_type_id <= 0 or material_amount <= 0 or
                product_param1 <= 0 or product_param2 <= 0 or loss_percent < 0):
            return -1

        # Коэффициент типа продукции (в реальной системе получали бы из БД)
        product_type_coef = 1.0  # Здесь должна быть логика получения из БД

        # Расчет с учетом потерь
        effective_amount = material_amount * (1 - loss_percent / 100)
        material_per_product = product_param1 * product_param2 * product_type_coef

        if material_per_product <= 0:
            return -1

        return int(effective_amount / material_per_product)
    except:
        return -1