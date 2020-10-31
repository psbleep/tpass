import os

from collections import UserList


class StoreListing(UserList):
    def __init__(self, password_store_dir):
        self._password_store_dir = password_store_dir
        self._selected = 0
        self._search_term = ""
        self._file_listing = self._get_file_listing()
        self.data = self._file_listing

    def set_search_term(self, search_term):
        self._search_term = search_term
        self.data = self._get_file_listing_filtered_for_search_term(search_term)
        if self.selected > self._max_selected:
            self.selected = self._max_selected

    def refresh_file_listing(self):
        self._file_listing = self._get_file_listing()
        self.data = self._get_file_listing_filtered_for_search_term(self._search_term)

    def recalculate_selected(self):
        if self._selected < 0:
            self._selected = 0
        elif self._selected > self._max_selected:
            self._selected = self._max_selected

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._selected = val
        self.recalculate_selected()

    @property
    def selected_password(self):
        if self.data:
            return self.data[self.selected]

    @selected_password.setter
    def selected_password(self, password_name):
        self.selected = self.data.index(password_name)

    def _get_file_listing(self):
        listing = set()
        for step in os.walk(self._password_store_dir):
            listing.update(self._process_step(*step))
        return sorted(list(listing))

    def _process_step(self, dirpath, _, files):
        rel_dir = os.path.relpath(dirpath, self._password_store_dir).strip("./")
        if rel_dir.startswith("2fa"):
            return []
        return [
            os.path.join(rel_dir, os.path.splitext(f)[0])
            for f in files
            if os.path.splitext(f)[1] == ".gpg"
        ]

    def _get_file_listing_filtered_for_search_term(self, search_term):
        return list(filter(lambda f: search_term in f, self._file_listing))

    @property
    def _max_selected(self):
        if len(self.data) == 0:
            return 0
        else:
            return len(self.data) - 1

    def __repr__(self):
        return "StoreListing({data!r})".format(data=self.data)
