from datetime import datetime

from tcg_player.service import TCGPlayer


def test_list_category_printings(session: TCGPlayer):
    results = session.list_category_printings(category_id=1)
    result = [x for x in results if x.printing_id == 1]
    assert len(result) == 1
    assert result[0].printing_id == 1
    assert result[0].name == "Normal"
    assert result[0].display_order == 1
    assert result[0].modified_on == datetime(2013, 4, 3, 11, 43, 38)
