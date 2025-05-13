#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
import sys
from typing import Final
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .utilities import _user_str_to_API_float

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

class BracketParser:
    """This class provides utilities for parsing strings that have square bracket [] delimited tokens.
    
    Nested bracket strings ([A][[B1][B2]]) are supported. The class operates on one depth at a time.
    Typically, you will just want to call BracketParser.Parse(string)."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_current_position",
        "_parse_string"
    ]

    # constants
    START_TAG: Final = "["
 
    END_TAG: Final = "]"

    def __init__(self, parse_string: str):
        """Initializes this to start parsing the given parse_string."""

        super().__init__()
        self._parse_string = parse_string
        self._current_position = 0

    def has_next_token(self) -> bool:
        """Determines if there is another token to be parsed."""

        # check for at end of _parse_string
        if (len(self._parse_string) - self._current_position == 0):
            return False

        # check for start tag as expected
        if(self._parse_string.find(self.START_TAG, self._current_position) != self._current_position):
            raise Exception("Unexpected state in BracketString (not at a start tag)")

        # find end tag
        endTagIndex: int = self.matching_end_tag_index(self._parse_string, self._current_position)
        if (endTagIndex == -1):
            raise Exception("Unexpected state in BracketString (missing end tag)")

        return True

    def next_token(self) -> str:
        """Returns the next token of the parse string.
            
        has_next_token() should have returned true before calling this method.
        Note that the next token could itself be a nested parse string.
        """

        start_tag_index = self._current_position
        assert(start_tag_index == self._parse_string.find(self.START_TAG, self._current_position))

        end_tag_index = self.matching_end_tag_index(self._parse_string, start_tag_index)
        assert(end_tag_index > -1)

        # get the bracketed string
        token_string = self._parse_string[start_tag_index + len(self.START_TAG):end_tag_index]

        self._current_position = end_tag_index + len(self.END_TAG)

        return token_string

    def skip_token(self) -> bool:
        """Returns true if a token was successfully skipped, false otherwise."""

        start_tag_index = self._current_position
        assert(start_tag_index == self._parse_string.find(self.START_TAG, self._current_position))

        end_tag_index = self.matching_end_tag_index(self._parse_string, start_tag_index)
        if(end_tag_index <= -1):
            return False

        self._current_position = end_tag_index + len(self.END_TAG)

        return True

    def count_remaining_tokens(self) -> int:
        """Determines (and returns) the number of tokens remaining."""

        saved_position = self._current_position

        token_count = 0
        while(self.has_next_token()):
            token_count += 1
            self.skip_token()

        self._current_position = saved_position
        return token_count

    # CLASS METHODS

    @classmethod
    def is_valid_parse_string(cls, parse_string: str) -> bool:
        """Determines if the given parse_string is a valid parse string."""

        if(len(parse_string) == 0):
            return True

        # check for start tag as expected at beginning
        if(parse_string.find(cls.START_TAG, 0) != 0):
            return False

        # loop through each token and check that the start and end tags are appropriate
        start_tag_index = 0
        while(True):
            end_tag_index = cls.matching_end_tag_index(parse_string, start_tag_index)
            if(end_tag_index == -1):
                return False

            expected_start_tag_index = end_tag_index + len(cls.END_TAG)

            # at end with no errors?
            if(expected_start_tag_index >= len(parse_string)):
                return True

            start_tag_index = parse_string.find(cls.START_TAG, expected_start_tag_index)

            if(start_tag_index != expected_start_tag_index):
                return False

    @classmethod
    def matching_end_tag_index(cls, parse_string: str, start_tag_index: int) -> int:
        """Finds the index of the end tag that matches the given start tag (index) for the given string."""

        assert(parse_string[start_tag_index: start_tag_index + len(cls.START_TAG)] == cls.START_TAG)

        #  we start off just after the start tag with a nesting level of one
        current_index = start_tag_index + len(cls.START_TAG)
        end_tag_index = -1
        nesting_level = 1

        # loop through the string looking for start and end tags,
        # a start tag increments the nesting level while an end tag
        # decrements the nesting level
        # if the nesting level never gets to zero, there is no matching end tag
        while (True):
            start_tag_index = parse_string.find(cls.START_TAG, current_index)
            end_tag_index = parse_string.find(cls.END_TAG, current_index)

            # if there aren't end tags, we're screwed
            if (end_tag_index == -1):
                return -1

            # for this method, a non-existent start tag is like one at infinity
            if (start_tag_index == -1):
                start_tag_index = sys.maxsize

            if (start_tag_index < end_tag_index):
                # nesting level goes up...
                current_index = start_tag_index + len(cls.START_TAG)
                nesting_level += 1
            else:
                # nesting level goes down....
                current_index = end_tag_index + len(cls.END_TAG)
                nesting_level -= 1
                if (nesting_level == 0):
                    return end_tag_index

    @classmethod
    def parse(cls, string_to_parse: str) -> List[str]:
        """Parses the given string into a list."""

        if(not cls.is_valid_parse_string(string_to_parse)):
            raise Exception("'{0}' is not a valid bracket string".format(string_to_parse))

        # could speed this up by using a singleton (need to look at Python's threading issues...)
        parser = BracketParser(string_to_parse)
        tokens: List[str] = []
        while(parser.has_next_token()):
            {
            tokens.append(parser.next_token())
            }

        return tokens

    @classmethod
    def parse_floats(cls, string_to_parse: str) -> List[float]:
        """Parses the given string into a list of floats.
        'infinite' values coming from the concept process are handled.
        """
        strings = BracketParser.parse(string_to_parse)

        float_list = []
        for string in strings:
            float_list.append(_user_str_to_API_float(string)) # may raise exception

        return float_list

