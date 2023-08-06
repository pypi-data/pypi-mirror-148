"""Microsoft Word review tools (comments, markup, etc.) with Python."""

from typing import Optional

from docxrev import com


def quit_word():
    """Quit Word."""
    com.COM_WORD.Quit()


def quit_word_safely():
    """Quit Word if no documents are open."""
    documents = com.try_com(
        com.COM_WORD.Documents,
        except_errors=[
            com.ERRORS["rpc_server_unavailable"],  # Word isn't open anymore anyways
        ],
    )
    if not documents.Count:
        quit_word()


def get_active_document(
    save_on_exit: Optional[bool] = True, close_on_exit: Optional[bool] = False
) -> com.Document:
    """Get the currently active document.

    Parameters
    ----------
    save_on_exit
        Whether to save the document when exiting a ``with`` context. **Default:**
        ``True``.
    close_on_exit
        Whether to close the document when exiting a ``with`` context. **Default:**
        ``False``.
    """

    return com.Document(
        com.COM_WORD.ActiveDocument.FullName, save_on_exit, close_on_exit
    )
