#!/usr/bin/python
# -*- coding: utf-8 -*-
# Taken from: https://github.com/solominh/python-stardict
import struct
import gzip


class IfoFileException(Exception):
    """Exception while parsing the .ifo file.
    Now version error in .ifo file is the only case raising this exception.
    """

    def __init__(self, description="IfoFileException raised"):
        """Constructor from a description string.

        Arguments:
        - `description`: a string describing the exception condition.
        """
        self._description = description

    def __str__(self):
        """__str__ method, return the description of exception occured.

        """
        return self._description


class IfoFileReader(object):
    """Read infomation from .ifo file and parse the infomation a dictionary.
    The structure of the dictionary is shown below:
    {key, value}
    """

    def __init__(self, filename):
        """Constructor from filename.

        Arguments:
        - `filename`: the filename of .ifo file of stardict.
        May raise IfoFileException during initialization.
        """
        self._ifo = dict()
        with open(filename, "rU", encoding='utf-8') as ifo_file:
            self._ifo["dict_title"] = ifo_file.readline()  # dictionary title
            line = ifo_file.readline()  # version info
            key, equal, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # check version info, raise an IfoFileException if error encounted
            if key != "version":
                raise IfoFileException(
                    "Version info expected in the second line of {!r:s}!".format(filename))
            if value != "2.4.2" and value != "3.0.0":
                raise IfoFileException(
                    "Version expected to be either 2.4.2 or 3.0.0, but {!r:s} read!".format(value))
            self._ifo[key] = value
            # read in other infomation in the file
            for line in ifo_file:
                key, equal, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                self._ifo[key] = value
            # check if idxoffsetbits should be discarded due to version info
            if self._ifo["version"] == "3.0.0" and "idxoffsetbits" in self._ifo:
                del self._ifo["version"]

    def get_ifo(self, key):
        """Get configuration value.

        Arguments:
        - `key`: configuration option name
        Return:
        - configuration value corresponding to the specified key if exists, otherwise False.
        """
        if key not in self._ifo:
            return False
        return self._ifo[key]


class IdxFileReader(object):
    """Read dictionary indexes from the .idx file and store the indexes in a list and a dictionary.
    The list contains each entry in the .idx file, with subscript indicating the entry's origin index in .idx file.
    The dictionary is indexed by word name, and the value is an integer or a list of integers pointing to
    the entry in the list.
    """

    def __init__(self, filename, compressed=False, index_offset_bits=32):
        """
        Note: filename.dict and filename.dict.dz have different indices

        Arguments:
        - `filename`: the filename of .idx file of stardict.
        - `compressed`: indicate whether the .idx file is compressed.
        - `index_offset_bits`: the offset field length in bits.
        """
        # Open file
        if compressed:
            with gzip.open(filename, "rb") as index_file:
                self._content = index_file.read()
        else:
            with open(filename, "rb") as index_file:
                self._content = index_file.read()

        # Init
        self._offset = 0
        self._index = 0
        self._index_offset_bits = index_offset_bits
        self._word_idx = {}
        self._index_idx = []

        # Indexing
        for word_str, word_data_offset, word_data_size, index in self:  # Call __iter__ function
            self._index_idx.append(
                (word_str, word_data_offset, word_data_size))
            if word_str in self._word_idx:
                self._word_idx[word_str].append(len(self._index_idx) - 1)
            else:
                self._word_idx[word_str] = [len(self._index_idx) - 1]

        # Clean up
        del self._content
        del self._index_offset_bits
        del self._index

    def __iter__(self):
        """Define the iterator interface.

        """
        return self

    def __next__(self):
        """Define the iterator interface.

        """
        # EOF
        if self._offset == len(self._content):
            raise StopIteration
        # Read word_str => end with \0
        end = self._content.find(b'\x00', self._offset)
        word_str = self._content[self._offset: end].decode('utf-8')
        self._offset = end + 1

        # Read word_data_offset => 32 or 64 bits
        word_data_offset = 0
        if self._index_offset_bits == 32:
            word_data_offset, = struct.unpack(
                "!I", self._content[self._offset:self._offset + 4])
            self._offset += 4
        elif self._index_offset_bits == 64:
            word_data_offset, = struct.unpack(
                "!I", self._content[self._offset:self._offset + 8])
            self._offset += 8
        else:
            raise ValueError

        # Read word_data_size => always 32 bits
        word_data_size = 0
        word_data_size, = struct.unpack(
            "!I", self._content[self._offset:self._offset + 4])
        self._offset += 4

        # Increase index
        self._index += 1

        return (word_str, word_data_offset, word_data_size, self._index)

    def get_index_by_num(self, number):
        """Get index infomation of a specified entry in .idx file by origin index.
        May raise IndexError if number is out of range.

        Arguments:
        - `number`: the origin index of the entry in .idx file
        Return:
        A tuple in form of (word_str, word_data_offset, word_data_size)
        """
        if number >= len(self._index_idx):
            raise IndexError("Index out of range! Acessing the {:d} index but totally {:d}".format(
                number, len(self._index_idx)))
        return self._index_idx[number]

    def get_index_by_word(self, word_str):
        """Get index infomation of a specified word entry.

        Arguments:
        - `word_str`: name of word entry.
        Return:
        Index infomation corresponding to the specified word if exists, otherwise False.
        The index infomation returned is a list of tuples, in form of [(word_data_offset, word_data_size) ...]
        """
        if word_str not in self._word_idx:
            return []
        numbers = self._word_idx[word_str]
        indexes = []
        for number in numbers:
            indexes.append(self._index_idx[number][1:])
        return indexes

    def get_all_words(self):
        """Get all words in an dictionary

        Return:
        A set of words
        """

        return {data[0] for data in self._index_idx}


class DictFileReader(object):
    """Read the .dict file, store the data in memory for querying.
    """

    def __init__(self, filename, dict_ifo, dict_index, compressed=False):
        """Constructor.

        Arguments:
        - `filename`: filename of .dict file.
        - `dict_ifo`: IfoFileReader object.
        - `dict_index`: IdxFileReader object.
        """
        self._dict_ifo = dict_ifo
        self._dict_index = dict_index
        self._compressed = compressed
        self._offset = 0
        if self._compressed:
            with gzip.open(filename, "rb") as dict_file:
                self._dict_file = dict_file.read()
        else:
            with open(filename, "rb") as dict_file:
                self._dict_file = dict_file.read()

    def get_dict_by_word(self, word):
        """Get the word's dictionary data by it's name.

        Arguments:
        - `word`: word name.
        Return:
        The specified word's dictionary data, in form of dict as below:
        {type_identifier: infomation, ...}
        in which type_identifier can be any character in "mlgtxykwhnrWP".
        """
        result = []
        indexes = self._dict_index.get_index_by_word(word)
        if not indexes:
            return result
        # sametypesequence = m => same type_identifier = m
        sametypesequence = self._dict_ifo.get_ifo("sametypesequence")
        for index in indexes:
            self._offset = index[0]
            size = index[1]
            if sametypesequence:
                result.append(self._get_entry_sametypesequence(size))
            else:
                result.append(self._get_entry(size))
        return result

    def get_dict_by_index(self, index):
        """Get the word's dictionary data by it's index infomation.

        Arguments:
        - `index`: index of a word entrt in .idx file.'
        Return:
        The specified word's dictionary data, in form of dict as below:
        {type_identifier: infomation, ...}
        in which type_identifier can be any character in "mlgtxykwhnrWP".
        """
        word, offset, size = self._dict_index.get_index_by_num(index)
        self._offset = offset
        sametypesequence = self._dict_ifo.get_ifo("sametypesequence")
        if sametypesequence:
            return self._get_entry_sametypesequence(size)
        else:
            return self._get_entry(size)

    def _get_entry(self, size):
        result = {}
        read_size = 0
        start_offset = self._offset
        while read_size < size:
            type_identifier = struct.unpack("!c")
            if type_identifier in "mlgtxykwhnr":
                result[type_identifier] = self._get_entry_field_null_trail()
            else:
                result[type_identifier] = self._get_entry_field_size()
            read_size = self._offset - start_offset
        return result

    def _get_entry_sametypesequence(self, size):
        start_offset = self._offset
        result = {}
        sametypesequence = self._dict_ifo.get_ifo("sametypesequence")
        for k in range(0, len(sametypesequence)):
            if sametypesequence[k] in "mlgtxykwhnr":
                if k == len(sametypesequence) - 1:
                    result[sametypesequence[k]] = self._get_entry_field_size(
                        size - (self._offset - start_offset))
                else:
                    result[sametypesequence[k]
                           ] = self._get_entry_field_null_trail()
            elif sametypesequence[k] in "WP":
                if k == len(sametypesequence) - 1:
                    result[sametypesequence[k]] = self._get_entry_field_size(
                        size - (self._offset - start_offset))
                else:
                    result[sametypesequence[k]] = self._get_entry_field_size()
        return result

    def _get_entry_field_null_trail(self):
        end = self._dict_file.find(b'\x00', self._offset)
        result = self._dict_file[self._offset:end]
        self._offset = end + 1
        return result

    def _get_entry_field_size(self, size=None):
        if size is None:
            size = struct.unpack("!I", self._dict_file[
                                 self._offset:self._offset + 4])
            self._offset += 4
        result = self._dict_file[
            self._offset:self._offset + size]
        self._offset += size
        return result
