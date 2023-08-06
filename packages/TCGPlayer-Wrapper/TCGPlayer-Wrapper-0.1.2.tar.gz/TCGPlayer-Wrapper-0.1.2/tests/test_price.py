from tcg_player.service import TCGPlayer


def test_list_group_prices(session: TCGPlayer):
    results = session.list_group_prices(group_id=2324)
    result = [x for x in results if x.product_id == 175065]
    assert len(result) == 1
    assert result[0].product_id == 175065
    assert result[0].low_price == 99.99
    assert result[0].mid_price == 107.49
    assert result[0].high_price == 114.99
    assert result[0].market_price == 87.69
    assert result[0].direct_low_price is None
    assert result[0].sub_type_name == "Normal"


def test_product_prices(session: TCGPlayer):
    results = session.product_prices(product_id=175065)
    assert results[0].product_id == 175065
    assert results[0].low_price == 99.99
    assert results[0].mid_price == 107.49
    assert results[0].high_price == 114.99
    assert results[0].market_price == 87.69
    assert results[0].direct_low_price is None
    assert results[0].sub_type_name == "Normal"
