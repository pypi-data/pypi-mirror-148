from tcg_player.service import TCGPlayer


def test_list_category_conditions(session: TCGPlayer):
    results = session.list_category_conditions(category_id=2)
    result = [x for x in results if x.condition_id == 1]
    assert len(result) == 1
    assert result[0].condition_id == 1
    assert result[0].name == "Near Mint"
    assert result[0].abbreviation == "NM"
    assert result[0].display_order == 1
