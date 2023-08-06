Convenience functions for editing things.
- Cameron Simpson <cs@cskk.id.au> 02jun2016

*Latest release 20220429*:
New edit_obj to edit an object, usually in JSON format.

## Function `choose_editor(editor=None, environ=None)`

Choose an editor,
honouring the `$EDITOR` environment variable.

Parameters:
* `editor`: optional editor,
  default from `environ['EDITOR']`
  or from `EDITOR` (`'vi'`).
* `environ`: optional environment mapping,
  default `os.environ`

## Function `edit(lines, editor=None, environ=None)`

Write lines to a temporary file, edit the file, return the new lines.

The editor is chosen by `choose_editor(editor=editor,environ=environ)`.

## Function `edit_obj(o, editor=None, environ=None, to_text=None, from_text=None)`

Edit the cotents of an object `o`.
Return a new object containing the editing contents.
The default transcription is as JSON.

The editor is chosen by `choose_editor(editor=editor,environ=environ)`.

Parameters:
* `o`: the object whose
* `to_text`: the transcription function of the object to text;
  default `json.dumps`
* `from_text`: the transcription function of the object to text;
  default `json.loads`

## Function `edit_strings(strs, editor=None, environ=None)`

Edit an iterable list of `str`, return tuples of changed string pairs.

The editor is chosen by `choose_editor(editor=editor,environ=environ)`.

# Release Log



*Release 20220429*:
New edit_obj to edit an object, usually in JSON format.

*Release 20191201.1*:
Initial PyPI release: assorted functions for invoking editors on strings.
