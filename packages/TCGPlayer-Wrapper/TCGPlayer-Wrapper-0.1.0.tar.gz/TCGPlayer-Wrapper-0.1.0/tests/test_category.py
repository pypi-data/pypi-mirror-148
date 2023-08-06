from datetime import datetime

from tcg_player.service import TCGPlayer


def test_list_categories(session: TCGPlayer):
    results = session.list_categories()
    result = [x for x in results if x.category_id == 1]
    assert len(result) == 1
    assert result[0].category_id == 1
    assert result[0].name == "Magic"
    assert result[0].modified_on == datetime(2022, 4, 18, 13, 4, 52)
    assert result[0].display_name == "Magic: The Gathering"
    assert result[0].seo_category_name == "Magic the Gathering TCG (MTG)"
    assert result[0].sealed_label == "Sealed Products"
    assert result[0].non_sealed_label == "Single Cards"
    assert result[0].condition_guide_url == "https://store.tcgplayer.com/conditions/magic.aspx"
    assert result[0].is_scannable is True
    assert result[0].popularity == 7233794
    assert result[0].is_direct is True


def test_category(session: TCGPlayer):
    result = session.category(category_id=62)
    assert result.category_id == 62
    assert result.name == "Flesh & Blood TCG"
    assert result.modified_on == datetime(2022, 4, 14, 21, 45, 49)
    assert result.display_name == "Flesh and Blood TCG"
    assert result.seo_category_name == "Flesh and Blood TCG"
    assert result.sealed_label == "Sealed Products"
    assert result.non_sealed_label == "Cards"
    assert result.condition_guide_url == "https://store.tcgplayer.com/"
    assert result.is_scannable is True
    assert result.popularity == 0
    assert result.is_direct is False
