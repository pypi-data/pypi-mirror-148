from datetime import date, datetime

from tcg_player.service import TCGPlayer


def test_list_category_groups(session: TCGPlayer):
    results = session.list_category_groups(category_id=1)
    result = [x for x in results if x.group_id == 1882]
    assert len(result) == 1
    assert result[0].group_id == 1882
    assert result[0].name == "Amonkhet"
    assert result[0].abbreviation == "AKH"
    assert result[0].is_supplemental is False
    assert result[0].published_on == date(2017, 4, 28)
    assert result[0].modified_on == datetime(2022, 4, 27, 17, 47, 11)
    assert result[0].category_id == 1


def test_group(session: TCGPlayer):
    result = session.group(group_id=1)
    assert result.group_id == 1
    assert result.name == "10th Edition"
    assert result.abbreviation == "10E"
    assert result.is_supplemental is False
    assert result.published_on == date(2007, 7, 13)
    assert result.modified_on == datetime(2022, 4, 27, 9, 50, 17)
    assert result.category_id == 1
