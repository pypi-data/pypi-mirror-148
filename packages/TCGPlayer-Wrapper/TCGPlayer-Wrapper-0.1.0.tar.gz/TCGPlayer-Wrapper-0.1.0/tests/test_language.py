from tcg_player.service import TCGPlayer


def test_list_category_languages(session: TCGPlayer):
    results = session.list_category_languages(category_id=1)
    result = [x for x in results if x.language_id == 1]
    assert len(result) == 1
    assert result[0].language_id == 1
    assert result[0].name == "English"
    assert result[0].abbreviation == "EN"
