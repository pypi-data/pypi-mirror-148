from datetime import datetime

from tcg_player.service import TCGPlayer


def test_list_group_products(session: TCGPlayer):
    results = session.list_group_products(category_id=1, group_id=87)
    result = [x for x in results if x.product_id == 86]
    assert len(result) == 1
    assert result[0].product_id == 86
    assert result[0].name == "Abyssal Nightstalker"
    assert result[0].clean_name == "Abyssal Nightstalker"
    assert result[0].image_url == "https://tcgplayer-cdn.tcgplayer.com/product/86_200w.jpg"
    assert result[0].category_id == 1
    assert result[0].group_id == 87
    assert (
        result[0].url
        == "https://www.tcgplayer.com/product/86/magic-portal-second-age-abyssal-nightstalker"
    )
    assert result[0].modified_on == datetime(2022, 3, 9, 14, 45, 52)


def test_product(session: TCGPlayer):
    result = session.product(product_id=86)
    assert result.product_id == 86
    assert result.name == "Abyssal Nightstalker"
    assert result.clean_name == "Abyssal Nightstalker"
    assert result.image_url == "https://tcgplayer-cdn.tcgplayer.com/product/86_200w.jpg"
    assert result.category_id == 1
    assert result.group_id == 87
    assert (
        result.url
        == "https://www.tcgplayer.com/product/86/magic-portal-second-age-abyssal-nightstalker"
    )
    assert result.modified_on == datetime(2022, 3, 9, 14, 45, 52)
