# MIT License
#
# Copyright (c) 2024, Justin Randall, Smart Interactive Transformations Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytest

from interacticore.parsers.brokenjsonparser import fix_remove_output_header


@pytest.mark.parametrize("test_name, in_str, expected", [
    #  Test 1
    ("Test 1",
     """Here is the response formatted as the specified JSON schema:

{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}""",
     """{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}""",
     ),
    #  Test 2
    ("Test 2",
     """```json
{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}
```""",
     """```json
{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}
```""",
     ),
    #  Test 3
    ("Test 3",
     """Here is the response formatted as the specified JSON schema:

```json
{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}
```""",
     """```json
{
  "utterances": [
    "Thanks a ton, you rock!",
    "Really appreciate the help.",
    "Couldn't have done it without ya, thanks!",
    "You're the best, thanks a bunch!",
    "So grateful for your support, thanks.",
    "Appreciate you taking the time, thanks!",
    "Your help's been invaluable, thanks a mil!",
    "Can't thank you enough for the guidance.",
    "Thanks for being so patient and helpful.",
    "Truly appreciate you going above and beyond.",
    "Thanks for always being there to help.",
    "You make it so easy, thank you!",
    "Appreciate your expertise and willingness.",
    "Thanks for the great service.",
    "Your support means everything, thanks!",
    "Impressed with your helpfulness, thanks!",
    "You've been amazing, can't thank you enough.",
    "Thanks for the dedication in assisting me.", 
    "Sincerely appreciate the fantastic help.",
    "You're a lifesaver, thanks for the hard work!"
  ]
}
```""",
     ),
])
def test_fix_remove_output_header(test_name: str, in_str: str, expected: str):
    result = fix_remove_output_header(in_str)
    if result != expected:
        print(f"{test_name}: result: {result}")
    assert result == expected
