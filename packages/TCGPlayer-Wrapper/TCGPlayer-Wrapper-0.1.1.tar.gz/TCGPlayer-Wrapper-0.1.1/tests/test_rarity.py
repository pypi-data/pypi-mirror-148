from tcg_player.service import TCGPlayer


def test_list_category_rarities(session: TCGPlayer):
    results = session.list_category_rarities(category_id=1)
    result = [x for x in results if x.rarity_id == 3]
    assert len(result) == 1
    assert result[0].rarity_id == 3
    assert result[0].display_text == "Uncommon"
    assert result[0].db_value == "U"
