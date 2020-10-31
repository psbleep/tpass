import pytest

from tpass.store_listing import StoreListing

from tests import TEST_PASSWORD_STORE_DIR, REFRESH_TEST_PASSWORD_STORE_DIR


def test_set_listing_empty_search_term():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    assert listing.data == ["1", "2", "a", "b/a", "b/b", "c"]


def test_selected_index():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    assert listing.selected == 0


def test_set_selected_index():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected = 2
    assert listing.selected == 2


def test_set_selected_index_with_incrementer():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected += 3
    assert listing.selected == 3


def test_set_selected_index_below_zero():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected = -2
    assert listing.selected == 0


def test_set_selected_index_above_number_of_store_listings():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected = 6
    assert listing.selected == 5


def test_selected_password():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected = 2
    assert listing.selected_password == "a"


def test_selected_password_no_listing():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.data = []
    assert listing.selected_password is None


def test_set_selected_password():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected_password = "b/b"
    assert listing.selected == 4


def test_set_selected_password_is_not_in_listing():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    with pytest.raises(ValueError):
        listing.selected_password = "nonsense"


def test_set_search_term():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.set_search_term("c")
    assert listing.data == ["c"]


def test_set_search_term_selected_is_now__out_of_range():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing.selected = 2
    listing.set_search_term("b")
    assert listing.selected == 1


def test_refresh_file_listing():
    listing = StoreListing(password_store_dir=TEST_PASSWORD_STORE_DIR)
    listing._password_store_dir = REFRESH_TEST_PASSWORD_STORE_DIR
    listing.refresh_file_listing()
    assert listing.data == ["refresh"]
