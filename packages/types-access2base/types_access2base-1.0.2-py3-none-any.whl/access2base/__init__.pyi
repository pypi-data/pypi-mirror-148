# -*- coding: utf-8 -*-
"""
The access2base.py module implements an interface between Python (user) scripts and the Access2Base Basic library.

Usage:
    from access2base import *
Additionally, if Python and LibreOffice are started in separate processes:
    If LibreOffice started from console ... (example for Linux)
        ./soffice --accept='socket,host=localhost,port=2019;urp;'
    then insert next statement
        A2BConnect(hostname = 'localhost', port = 2019)

Specific documentation about Access2Base and Python:
    http://www.access2base.com/access2base.html#%5B%5BAccess2Base%20and%20Python%5D%5D
"""
from __future__ import annotations
import uno
from com.sun.star.awt import XControlModel, XControl, FontWeight as UnoFontWeight
from com.sun.star.awt import KeyFunction as UnoKeyFunction
from com.sun.star.awt import XWindow
from com.sun.star.drawing import LineStyle as UnoLineStyle
from com.sun.star.form import ListSourceType as UnoListSourceType
from com.sun.star.form.component import FixedText, GroupBox, DataForm
from com.sun.star.frame import Desktop as UnoDesktop
from com.sun.star.script.provider import XScript as UnoXScript
from com.sun.star.script.provider import XScriptProvider as UnoXScriptProvider
from com.sun.star.sdb import Column as UnoColumn
from com.sun.star.sdb import OfficeDatabaseDocument, ResultSet
from com.sun.star.sdbc import XConnection, XDatabaseMetaData
from com.sun.star.sdbc import RowSet as UnoRowSet
from com.sun.star.sdbcx import Table as UnoTable
from com.sun.star.text import TextDocument as UnoTextDocument
from com.sun.star.uno import XComponentContext as UnoXComponentContext
from com.sun.star.uno import XInterface as UnoXInterface
from types import TracebackType
from typing import Any, Tuple, Type, Optional, overload, Union
from typing_extensions import Literal, Self
from numbers import Number
import datetime
import time

XSCRIPTCONTEXT: uno


class _Singleton(type):
    """
    A Singleton design pattern
    Credits: « Python in a Nutshell » by Alex Martelli, O'Reilly
    """

    def __call__(cls, *args: Any, **kwargs: Any) -> Self: ...


class acConstants(object, metaclass=_Singleton):
    """
    VBA constants used in the Access2Base API.
    Values derived from MSAccess, except when conflicts
    """
    # Python special constants (used in the protocol between Python and Basic)
    # -----------------------------------------------------------------
    Empty: Literal["+++EMPTY+++"]
    Null: Literal["+++NULL+++"]
    Missing: Literal["+++MISSING+++"]
    FromIsoFormat: Literal[
        "%Y-%m-%d %H:%M:%S"
    ]  # To be used with datetime.datetime.strptime()

    # AcCloseSave
    # -----------------------------------------------------------------
    acSaveNo: Literal[2]
    acSavePrompt: Literal[0]
    acSaveYes: Literal[1]

    # AcFormView
    # -----------------------------------------------------------------
    acDesign: Literal[1]
    acNormal: Literal[0]
    acPreview: Literal[2]

    # AcFormOpenDataMode
    # -----------------------------------------------------------------
    acFormAdd: Literal[0]
    acFormEdit: Literal[1]
    acFormPropertySettings: Literal[-1]
    acFormReadOnly: Literal[2]

    # acView
    # -----------------------------------------------------------------
    acViewDesign: Literal[1]
    acViewNormal: Literal[0]
    acViewPreview: Literal[2]

    # acOpenDataMode
    # -----------------------------------------------------------------
    acAdd: Literal[0]
    acEdit: Literal[1]
    acReadOnly: Literal[2]

    # AcObjectType
    # -----------------------------------------------------------------
    acDefault: Literal[-1]
    acDiagram: Literal[8]
    acForm: Literal[2]
    acQuery: Literal[1]
    acReport: Literal[3]
    acTable: Literal[0]
    #   Unexisting in MS/Access
    acBasicIDE: Literal[101]
    acDatabaseWindow: Literal[102]
    acDocument: Literal[111]
    acWelcome: Literal[112]
    #   Subtype if acDocument
    docWriter: Literal["Writer"]
    docCalc: Literal["Calc"]
    docImpress: Literal["Impress"]
    docDraw: Literal["Draw"]
    docMath: Literal["Math"]

    # AcWindowMode
    # -----------------------------------------------------------------
    acDialog: Literal[3]
    acHidden: Literal[1]
    acIcon: Literal[2]
    acWindowNormal: Literal[0]

    # VarType constants
    # -----------------------------------------------------------------
    vbEmpty: Literal[0]
    vbNull: Literal[1]
    vbInteger: Literal[2]
    vbLong: Literal[3]
    vbSingle: Literal[4]
    vbDouble: Literal[5]
    vbCurrency: Literal[6]
    vbDate: Literal[7]
    vbString: Literal[8]
    vbObject: Literal[9]
    vbBoolean: Literal[11]
    vbVariant: Literal[12]
    vbByte: Literal[17]
    vbUShort: Literal[18]
    vbULong: Literal[19]
    vbBigint: Literal[35]
    vbDecimal: Literal[37]
    vbArray: Literal[8192]

    # MsgBox constants
    # -----------------------------------------------------------------
    vbOKOnly: Literal[0]  # OK button only (default)
    vbOKCancel: Literal[1]  # OK and Cancel buttons]
    vbAbortRetryIgnore: Literal[2]  # Abort, Retry, and Ignore buttons
    vbYesNoCancel: Literal[3]  # Yes, No, and Cancel buttons
    vbYesNo: Literal[4]  # Yes and No buttons
    vbRetryCancel: Literal[5]  # Retry and Cancel buttons
    vbCritical: Literal[16]  # Critical message
    vbQuestion: Literal[32]  # Warning query
    vbExclamation: Literal[48]  # Warning message
    vbInformation: Literal[64]  # Information message
    vbDefaultButton1: Literal[128]  # First button is default (default) (VBA: 0)
    vbDefaultButton2: Literal[256]  # Second button is default
    vbDefaultButton3: Literal[512]  # Third button is default
    vbApplicationModal: Literal[0]  # Application modal message box (default)
    # MsgBox Return Values
    # -----------------------------------------------------------------
    vbOK: Literal[1]  # OK button pressed
    vbCancel: Literal[2]  # Cancel button pressed
    vbAbort: Literal[3]  # Abort button pressed
    vbRetry: Literal[4]  # Retry button pressed
    vbIgnore: Literal[5]  # Ignore button pressed
    vbYes: Literal[6]  # Yes button pressed
    vbNo: Literal[7]  # No button pressed

    # Dialogs Return Values
    # ------------------------------------------------------------------
    dlgOK: Literal[1]  # OK button pressed
    dlgCancel: Literal[0]  # Cancel button pressed

    # Control Types
    # -----------------------------------------------------------------
    acCheckBox: Literal[5]
    acComboBox: Literal[7]
    acCommandButton: Literal[2]
    acToggleButton: Literal[122]
    acCurrencyField: Literal[18]
    acDateField: Literal[15]
    acFileControl: Literal[12]
    acFixedLine: Literal[24]  # FREE ENTRY (USEFUL IN DIALOGS)
    acFixedText: Literal[10]
    acLabel: Literal[10]
    acFormattedField: Literal[1]  # FREE ENTRY TAKEN TO NOT CONFUSE WITH acTextField
    acGridControl: Literal[11]
    acGroupBox: Literal[8]
    acOptionGroup: Literal[8]
    acHiddenControl: Literal[13]
    acImageButton: Literal[4]
    acImageControl: Literal[14]
    acImage: Literal[14]
    acListBox: Literal[6]
    acNavigationBar: Literal[22]
    acNumericField: Literal[17]
    acPatternField: Literal[19]
    acProgressBar: Literal[23]  # FREE ENTRY (USEFUL IN DIALOGS)
    acRadioButton: Literal[3]
    acOptionButton: Literal[3]
    acScrollBar: Literal[20]
    acSpinButton: Literal[21]
    acSubform: Literal[112]
    acTextField: Literal[9]
    acTextBox: Literal[9]
    acTimeField: Literal[16]

    # AcRecord
    # -----------------------------------------------------------------
    acFirst: Literal[2]
    acGoTo: Literal[4]
    acLast: Literal[3]
    acNewRec: Literal[5]
    acNext: Literal[1]
    acPrevious: Literal[0]

    # FindRecord
    # -----------------------------------------------------------------
    acAnywhere: Literal[0]
    acEntire: Literal[1]
    acStart: Literal[2]
    acDown: Literal[1]
    acSearchAll: Literal[2]
    acUp: Literal[0]
    acAll: Literal[0]
    acCurrent: Literal[-1]

    # AcDataObjectType
    # -----------------------------------------------------------------
    acActiveDataObject: Literal[-1]
    acDataForm: Literal[2]
    acDataQuery: Literal[1]
    acDataServerView: Literal[7]
    acDataStoredProcedure: Literal[9]
    acDataTable: Literal[0]

    # AcQuitOption
    # -----------------------------------------------------------------
    acQuitPrompt: Literal[0]
    acQuitSaveAll: Literal[1]
    acQuitSaveNone: Literal[2]

    # AcCommand
    # -----------------------------------------------------------------
    acCmdAboutMicrosoftAccess: Literal[35]
    acCmdAboutOpenOffice: Literal[35]
    acCmdAboutLibreOffice: Literal[35]
    acCmdVisualBasicEditor: Literal[525]
    acCmdBringToFront: Literal[52]
    acCmdClose: Literal[58]
    acCmdToolbarsCustomize: Literal[165]
    acCmdChangeToCommandButton: Literal[501]
    acCmdChangeToCheckBox: Literal[231]
    acCmdChangeToComboBox: Literal[230]
    acCmdChangeToTextBox: Literal[227]
    acCmdChangeToLabel: Literal[228]
    acCmdChangeToImage: Literal[234]
    acCmdChangeToListBox: Literal[229]
    acCmdChangeToOptionButton: Literal[233]
    acCmdCopy: Literal[190]
    acCmdCut: Literal[189]
    acCmdCreateRelationship: Literal[150]
    acCmdDelete: Literal[337]
    acCmdDatabaseProperties: Literal[256]
    acCmdSQLView: Literal[184]
    acCmdRemove: Literal[366]
    acCmdDesignView: Literal[183]
    acCmdFormView: Literal[281]
    acCmdNewObjectForm: Literal[136]
    acCmdNewObjectTable: Literal[134]
    acCmdNewObjectView: Literal[350]
    acCmdOpenDatabase: Literal[25]
    acCmdNewObjectQuery: Literal[135]
    acCmdShowAllRelationships: Literal[149]
    acCmdNewObjectReport: Literal[137]
    acCmdSelectAll: Literal[333]
    acCmdRemoveTable: Literal[84]
    acCmdOpenTable: Literal[221]
    acCmdRename: Literal[143]
    acCmdDeleteRecord: Literal[223]
    acCmdApplyFilterSort: Literal[93]
    acCmdSnapToGrid: Literal[62]
    acCmdViewGrid: Literal[63]
    acCmdInsertHyperlink: Literal[259]
    acCmdMaximumRecords: Literal[508]
    acCmdObjectBrowser: Literal[200]
    acCmdPaste: Literal[191]
    acCmdPasteSpecial: Literal[64]
    acCmdPrint: Literal[340]
    acCmdPrintPreview: Literal[54]
    acCmdSaveRecord: Literal[97]
    acCmdFind: Literal[30]
    acCmdUndo: Literal[292]
    acCmdRefresh: Literal[18]
    acCmdRemoveFilterSort: Literal[144]
    acCmdRunMacro: Literal[31]
    acCmdSave: Literal[20]
    acCmdSaveAs: Literal[21]
    acCmdSelectAllRecords: Literal[109]
    acCmdSendToBack: Literal[53]
    acCmdSortDescending: Literal[164]
    acCmdSortAscending: Literal[163]
    acCmdTabOrder: Literal[41]
    acCmdDatasheetView: Literal[282]
    acCmdZoomSelection: Literal[371]

    # AcSendObjectType
    # -----------------------------------------------------------------
    acSendForm: Literal[2]
    acSendNoObject: Literal[-1]
    acSendQuery: Literal[1]
    acSendReport: Literal[3]
    acSendTable: Literal[0]

    # AcOutputObjectType
    # -----------------------------------------------------------------
    acOutputTable: Literal[0]
    acOutputQuery: Literal[1]
    acOutputForm: Literal[2]
    acOutputArray: Literal[-1]

    # AcEncoding
    # -----------------------------------------------------------------
    acUTF8Encoding: Literal[76]

    # AcFormat
    # -----------------------------------------------------------------
    acFormatPDF: Literal["writer_pdf_Export"]
    acFormatODT: Literal["writer8"]
    acFormatDOC: Literal["MS Word 97"]
    acFormatHTML: Literal["HTML"]
    acFormatODS: Literal["calc8"]
    acFormatXLS: Literal["MS Excel 97"]
    acFormatXLSX: Literal["Calc MS Excel 2007 XML"]
    acFormatTXT: Literal["Text - txt - csv (StarCalc)"]

    # AcExportQuality
    # -----------------------------------------------------------------
    acExportQualityPrint: Literal[0]
    acExportQualityScreen: Literal[1]

    # AcSysCmdAction
    # -----------------------------------------------------------------
    acSysCmdAccessDir: Literal[9]
    acSysCmdAccessVer: Literal[7]
    acSysCmdClearHelpTopic: Literal[11]
    acSysCmdClearStatus: Literal[5]
    acSysCmdGetObjectState: Literal[10]
    acSysCmdGetWorkgroupFile: Literal[13]
    acSysCmdIniFile: Literal[8]
    acSysCmdInitMeter: Literal[1]
    acSysCmdProfile: Literal[12]
    acSysCmdRemoveMeter: Literal[3]
    acSysCmdRuntime: Literal[6]
    acSysCmdSetStatus: Literal[4]
    acSysCmdUpdateMeter: Literal[2]

    # Type property
    # -----------------------------------------------------------------
    dbBigInt: Literal[16]
    dbBinary: Literal[9]
    dbBoolean: Literal[1]
    dbByte: Literal[2]
    dbChar: Literal[18]
    dbCurrency: Literal[5]
    dbDate: Literal[8]
    dbDecimal: Literal[20]
    dbDouble: Literal[7]
    dbFloat: Literal[21]
    dbGUID: Literal[15]
    dbInteger: Literal[3]
    dbLong: Literal[4]
    dbLongBinary: Literal[11]  # (OLE Object)
    dbMemo: Literal[12]
    dbNumeric: Literal[19]
    dbSingle: Literal[6]
    dbText: Literal[10]
    dbTime: Literal[22]
    dbTimeStamp: Literal[23]
    dbVarBinary: Literal[17]
    dbUndefined: Literal[-1]

    # Attributes property
    # -----------------------------------------------------------------
    dbAutoIncrField: Literal[16]
    dbDescending: Literal[1]
    dbFixedField: Literal[1]
    dbHyperlinkField: Literal[32768]
    dbSystemField: Literal[8192]
    dbUpdatableField: Literal[32]
    dbVariableField: Literal[2]

    # OpenRecordset
    # -----------------------------------------------------------------
    dbOpenForwardOnly: Literal[8]
    dbSQLPassThrough: Literal[64]
    dbReadOnly: Literal[4]

    # Query types
    # -----------------------------------------------------------------
    dbQAction: Literal[240]
    dbQAppend: Literal[64]
    dbQDDL: Literal[4]  # 96
    dbQDelete: Literal[32]
    dbQMakeTable: Literal[128]  # 80
    dbQSelect: Literal[0]
    dbQSetOperation: Literal[8]  # 128
    dbQSQLPassThrough: Literal[1]  # 112
    dbQUpdate: Literal[16]  # 48

    # Edit mode
    # -----------------------------------------------------------------
    dbEditNone: Literal[0]
    dbEditInProgress: Literal[1]
    dbEditAdd: Literal[2]

    # Toolbars
    # -----------------------------------------------------------------
    msoBarTypeNormal: Literal[0]  # Usual toolbar
    msoBarTypeMenuBar: Literal[1]  # Menu bar
    msoBarTypePopup: Literal[2]  # Shortcut menu
    msoBarTypeStatusBar: Literal[11]  # Status bar
    msoBarTypeFloater: Literal[12]  # Floating window

    msoControlButton: Literal[1]  # Command button
    msoControlPopup: Literal[10]  # Popup, submenu

    # New Lines
    # -----------------------------------------------------------------
    vbCr: Literal["\r"]
    vbLf: Literal["\n"]

    def _NewLine() -> str: ...

    vbNewLine: str
    vbTab: Literal["\t"]

    # Module types
    # -----------------------------------------------------------------
    acClassModule: Literal[1]
    acStandardModule: Literal[0]

    # (Module) procedure types
    # -----------------------------------------------------------------
    vbext_pk_Get: Literal[1]  # A Property Get procedure
    vbext_pk_Let: Literal[2]  # A Property Let procedure
    vbext_pk_Proc: Literal[0]  # A Sub or Function procedure
    vbext_pk_Set: Literal[3]  # A Property Set procedure


COMPONENTCONTEXT: UnoXComponentContext
DESKTOP: UnoDesktop
SCRIPTPROVIDER: UnoXScriptProvider
THISDATABASEDOCUMENT: OfficeDatabaseDocument


def _ErrorHandler(
        type: Type[Any], value: BaseException, tb: Union[TracebackType, None] = ...
) -> None:
    """
    Is the function to be set as new sys.excepthook to bypass the standard error handler
        Derived from https://stackoverflow.com/questions/31949760/how-to-limit-python-traceback-to-specific-files
    Handler removes traces pointing to methods located in access2base.py when error is due to a user programming error
        sys.excepthook = _ErrorHandler
    NOT APPLIED YET
    """


def A2BConnect(hostname: Optional[str] = ..., port: Optional[int] = ...) -> None:
    """
    To be called explicitly by user scripts when Python process runs outside the LibreOffice process.
        LibreOffice started as (Linux):
            ./soffice --accept='socket,host=localhost,port=xxxx;urp;'
    Otherwise called implicitly by the current module without arguments
    Initializes COMPONENTCONTEXT, SCRIPTPROVIDER and DESKTOP

    Args:
        hostname (Optional[str], optional): probably 'localhost' or ''. Defaults to ''
        port (Optional[int], optional): port number or 0. Defaults to 0
    """


class _A2B(object, metaclass=_Singleton):
    """
    Collection of helper functions implementing the protocol between Python and Basic
        Read comments in PythonWrapper Basic function
    """

    @classmethod
    def BasicObject(cls, objectname: str) -> Any: ...

    @classmethod
    def xScript(cls, script: str, module: str) -> UnoXScript:
        """
        At first call checks the existence of the Access2Base library
        Initializes _LIBRARY with the found library name
        First and next calls execute the given script in the given module of the _LIBRARY library
        The script and module are presumed to exist

        Args:
            script (str): name of script
            module (str): name of module

        Returns:
            XScript: interface represents an invocable script or UNO function.
        """

    @classmethod
    def A2BErrorCode(cls) -> object:
        """
        Return the Access2Base error stack as a tuple
            0 => error code
            1 => severity level
            2 => short error message
            3 => long error message
        """

    @classmethod
    def invokeMethod(cls, script: str, module: str, *args: Any) -> Union[Any, None]:
        """
        Direct call to a named script/module pair with their arguments
        If the arguments do not match their definition at the Basic side, a TypeError is raised

        Args:
            script (str): name of script
            module (str): name of module

        Other Args:
            *args (Any): list of arguments to be passed to the script

        Raises:
            TypeError: If there is error invoking.

        Returns:
            Any | None: the value returned by the script execution
        """

    @classmethod
    def invokeWrapper(cls, action: int, basic: int, script: str, *args: Any) -> Any:
        """
        Call the Basic wrapper to invite it to execute the proposed action on a Basic object
        If the arguments do not match their definition at the Basic side, a TypeError is raised
        After execution, a check is done if the execution has raised an error within Basic

        Args:
            action (int): Property Get, Property Let, Property Set, invoke Method or return UNO object
            basic (int): the reference of the Basic object, i.e. the index in the array caching the
                addresses of the objects conventionally Application = -1 and DoCmd = -2
            script (str): the property or method name

        Other Ars:
            *args (Any): the arguments of the method, if any

        Raises:
            TypeError: If there is error invoking.

        Returns:
            Any: the value returned by the execution of the Basic routine
        """

    @classmethod
    def VerifyNoError(cls) -> bool: ...


class Application(object, metaclass=_Singleton):
    """Collection of methods located in the Application (Basic) module"""

    # W = _A2B.invokeWrapper
    basicmodule: Literal[-1]

    @overload
    @classmethod
    def AllDialogs(cls) -> _Collection:
        """
        The AllDialogs collection describes instances of all dialogs present in the currently loaded dialog libraries.

        Returns:
            _Collection: A Collection object

        See Also:
            `AllDialogs <http://www.access2base.com/access2base.html#AllDialogs>`_
        """

    @overload
    @classmethod
    def AllDialogs(cls, dialog: int) -> _Dialog:
        """
        The AllDialogs collection describes instances of all dialogs present in the currently loaded dialog libraries.

        Args:
            dialog (str, optional): _description_. Defaults to ....

        Returns:
            _Dialog: A Dialog object corresponding to the index-th item in the AllDialogs() collection.
                The 1st dialog is AllDialogs(0), the 2nd is AllDialogs(1) and so on ...
                The last one is AllDialogs.Count - 1.

        See Also:
            `AllDialogs <http://www.access2base.com/access2base.html#AllDialogs>`_
        """

    @overload
    @classmethod
    def AllDialogs(cls, dialog: str) -> _Dialog:
        """
        The AllDialogs collection describes instances of all dialogs present in the currently loaded dialog libraries.

        Args:
            dialog (str, optional): _description_. Defaults to ....

        Returns:
            _Dialog: A Dialog object having the argument as name. The argument is NOT case-sensitive.

        See Also:
            `AllDialogs <http://www.access2base.com/access2base.html#AllDialogs>`_
        """

    @overload
    @classmethod
    def AllForms(cls) -> _Collection:
        """
        Describes instances of all forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing
        one or more standalone forms.

        Returns:
            _Collection: A Collection object

        See Also:
            `AllForms <http://www.access2base.com/access2base.html#AllForms>`_
        """

    @overload
    @classmethod
    def AllForms(cls, form: int) -> _Form:
        """
        Describes instances of all forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing
        one or more standalone forms.

        Args:
            form (str, int, optional): A Form object corresponding to the index-th item in the AllForms() collection.
                The 1st form is AllForms(0), the 2nd is AllForms(1) and so on ...
                The last one has as index AllForms.Count - 1.

        Returns:
            _Form: A Form object corresponding to the index-th item in the AllForms() collection.
                The 1st form is AllForms(0), the 2nd is AllForms(1) and so on ...
                The last one has as index AllForms.Count - 1.

        See Also:
            `AllForms <http://www.access2base.com/access2base.html#AllForms>`_
        """

    @overload
    @classmethod
    def AllForms(cls, form: str) -> _Form:
        """
        Describes instances of all forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing
        one or more standalone forms.

        Args:
            form (str, int, optional): A Form object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _Form: A Form object having the argument as name. The argument is NOT case-sensitive.

        See Also:
            `AllForms <http://www.access2base.com/access2base.html#AllForms>`_
        """

    @overload
    @classmethod
    def AllModules(cls) -> _Collection:
        """
        Describes instances of all modules present in the currently loaded Basic libraries.

        Returns:
            _Collection: A Collection object

        See Also:
            `AllModules <http://www.access2base.com/access2base.html#AllModules>`_
        """

    @overload
    @classmethod
    def AllModules(cls, module: int) -> _Module:
        """
        Describes instances of all modules present in the currently loaded Basic libraries.

        Args:
            module (int): A Module object corresponding to the index-th item in the AllModules() collection.
                The 1st module is AlModules(0), the 2nd is AllModules(1) and so on ...
                The last one is AllModules.Count - 1.

        Returns:
            _Module: A Module object.

        See Also:
            `AllModules <http://www.access2base.com/access2base.html#AllModules>`_
        """

    @overload
    @classmethod
    def AllModules(cls, module: str) -> _Module:
        """
        Describes instances of all modules present in the currently loaded Basic libraries.

        Args:
            module (int): A Module object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _Module: A Module object.

        See Also:
            `AllModules <http://www.access2base.com/access2base.html#AllModules>`_
        """

    @classmethod
    def CloseConnection(cls) -> None:
        """
        The invocation of the CloseConnection as a Sub is recommended
        but not mandatory before closing a document invoking the Access2Base API.

        See Also:
            `CloseConnection <http://www.access2base.com/access2base.html#CloseConnection>`_
        """

    @overload
    @classmethod
    def CommandBars(cls) -> _Collection:
        """
        The CommandBars collection describes instances of all toolbars or menu bars present
        in the currently selected document, whenever visible or hidden.

        Returns:
            _Collection: A Collection object

        See Also:
            `CommandBars <http://www.access2base.com/access2base.html#CommandBars>`_
        """

    @overload
    @classmethod
    def CommandBars(cls, bar: int) -> _CommandBar:
        """
        Gets a CommandBar object corresponding to the index.

        Args:
            bar (int): A CommandBar object corresponding to the index-th item in the
                CommandBars() collection. The 1st commandbar is CommandBars(0),
                the 2nd is CommandBars(1) and so on ... The last one is CommandBars.Count - 1.

        Returns:
            _CommandBar: A CommandBar object

        See Also:
            `CommandBars <http://www.access2base.com/access2base.html#CommandBars>`_
        """

    @overload
    @classmethod
    def CommandBars(cls, bar: str) -> _CommandBar:
        """
        Gets a CommandBar object corresponding to the ``bar``.

        Args:
            bar (str): A CommandBar object having the argument as name.
                The argument is NOT case-sensitive.

        Returns:
            _CommandBar: A CommandBar object

        See Also:
            `CommandBars <http://www.access2base.com/access2base.html#CommandBars>`_
        """

    @classmethod
    def CurrentDb(cls) -> Union[_Database, None]:
        """
        Gets the database object related to a Base (".odb") document.

        Returns:
            _Database | None: None if the database connection is undefined or is currently unavailable;
                Otherwise, _Database object.

        See Also:
            `CurrentDb <http://www.access2base.com/access2base.html#CurrentDb>`_
        """

    @classmethod
    def CurrentUser(cls) -> str:
        """
        Gets the logon name of the current user.

        Returns:
            str: user name

        See Also:
            `CurrentUser <http://www.access2base.com/access2base.html#CurrentUser>`_
        """

    @overload
    @classmethod
    def DAvg(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DAvg(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the average of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DAvg
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DAvg function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The average of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DAvg <http://www.access2base.com/access2base.html#DAvg>`_
        """

    @overload
    @classmethod
    def DCount(cls, expression: str, domain: str) -> Union[int, None]: ...
    @overload
    @classmethod
    def DCount(cls, expression: str, domain: str, criteria: str) -> Union[int, None]:
        """
        Gets the number of records that are in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DCount
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DCount function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            int | None: the number of records that are in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DCount <http://www.access2base.com/access2base.html#DCount>`_
        """

    @classmethod
    def DLookup(
            cls, expression: str, domain: str, criteria: str = ..., orderclause: str = ...
    ) -> Any:
        """
        Gets the value of a particular field from a specified set of records (a domain).

        You can use the DLookup function to display the value of a field that isn't in the record
        source for your form. For example, suppose you have a form based on an Order Details table.
        The form displays the OrderID, ProductID, UnitPrice, Quantity, and Discount fields.
        However, the ProductName field is in another table, the Products table.
        You could use the DLookup function in an event to display the ProductName on the same form.

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DLookup
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DLookup function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.
            orderclause (str, optional): A string expression specifying the sequence of the returned records.
                It is a SQL ORDER BY clause without the words ORDER BY. It can include the ASC or DESC keywords.

        Returns:
            Any: result

        See Also:
            `DLookup <http://www.access2base.com/access2base.html#DLookup>`_
        """

    @overload
    @classmethod
    def DMax(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DMax(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the maximum value of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DMax
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DMax function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: the maximum value of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DMax <http://www.access2base.com/access2base.html#%5B%5BDMin%2C%20DMax%5D%5D>`_
        """

    @overload
    @classmethod
    def DMin(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DMin(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the minimum value of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DMin
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DMin function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: the minimum value of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DMin <http://www.access2base.com/access2base.html#%5B%5BDMin%2C%20DMax%5D%5D>`_
        """

    @overload
    @classmethod
    def DStDev(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DStDev(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the standard deviation of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DStDev
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DStDev function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The standard deviation of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DStDev <http://www.access2base.com/access2base.html#%5B%5BDStDev%2C%20DStDevP%5D%5D>`_
        """

    @overload
    @classmethod
    def DStDevP(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DStDevP(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the standard deviation of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DStDevP
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DStDevP function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The standard deviation of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DStDevP <http://www.access2base.com/access2base.html#%5B%5BDStDev%2C%20DStDevP%5D%5D>`_
        """

    @overload
    @classmethod
    def DSum(cls, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    @classmethod
    def DSum(cls, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the sum of a set of numeric values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DSum
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DSum function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The sum of a set of numeric values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DSum <http://www.access2base.com/access2base.html#DSum>`_
        """

    @overload
    @classmethod
    def DVar(cls, expression: str, domain: str) -> Union[Any, None]: ...
    @overload
    @classmethod
    def DVar(cls, expression: str, domain: str, criteria: str) -> Union[Any, None]:
        """
        Gets the variance of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DVar
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DVar function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            Any | None: the variance of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DVar <http://www.access2base.com/access2base.html#%5B%5BDVar%2C%20DVarP%5D%5D>`_
        """

    @overload
    @classmethod
    def DVarP(cls, expression: str, domain: str) -> Union[Any, None]: ...
    @overload
    @classmethod
    def DVarP(cls, expression: str, domain: str, criteria: str) -> Union[Any, None]:
        """
        Gets the variance of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DVarP
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DVarP function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            Any | None: the variance of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DVarP <http://www.access2base.com/access2base.html#%5B%5BDVar%2C%20DVarP%5D%5D>`_
        """

    @classmethod
    def Events(cls, event: Any) -> Union[_Event, None]:
        """
        Gets the (unique) instance of the currently executed event object.

        Args:
            event (Any): The event argument is the variable of Variant/Object type given as argument by
                OpenOffice/LibreOffice to the macro invoked when the event occurs.

        Returns:
            _Event | None: the (unique) instance of the currently executed event object.
                Returns None when the event is not really an event or it was triggered by an unsupported event
                type - or some other error occurred (the call to Events() never stops the execution of the macro).
                In particular, when the event has been triggered by a toolbar button;
        """

    @overload
    @classmethod
    def Forms(cls) -> _Collection:
        """
        Describes instances of all open forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing one or more
        standalone forms.


        Returns:
            _Form: A Collection object

        See Also:
            `Forms <http://www.access2base.com/access2base.html#Forms>`_
        """

    @overload
    @classmethod
    def Forms(cls, form: int) -> _Form:
        """
        Describes instances of all open forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing one or more
        standalone forms.

        Args:
            form (int): A Form object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _Form: A Form object

        See Also:
            `Forms <http://www.access2base.com/access2base.html#Forms>`_
        """

    @overload
    @classmethod
    def Forms(cls, form: str) -> _Form:
        """
        Describes instances of all open forms present in the current Base document (".odb" file)
        or in the current non-Base document (".odt", ".ods", ... file) containing one or more
        standalone forms.

        Args:
            form (str): A Form object corresponding to the index-th item in the Forms() collection.
                The 1st form is Forms(0), the 2nd is Forms(1) and so on ... The last one is Forms.Count - 1.

        Returns:
            _Form: A Form object

        See Also:
            `Forms <http://www.access2base.com/access2base.html#Forms>`_
        """

    @classmethod
    def getObject(cls, shortcut: str) -> Any:
        """
        Gets an object designated by its shortcut notation.

        Args:
            shortcut (str): An object of types Form, Dialog or Control. Other types are currently not supported.

        Returns:
            Any: object

        See Also:
            `getObject <http://www.access2base.com/access2base.html#getObject>`_
        """

    GetObject = getObject

    @classmethod
    def getValue(cls, shortcut: str) -> Any:
        """
        Gets a property of an object designated by its shortcut notation.

        Args:
            shortcut (str): An object of types Form, Dialog or Control. Other types are currently not supported.

        Returns:
            Any: object

        See Also:
            `getValue <http://www.access2base.com/access2base.html#getValue>`_
        """

    GetValue = getValue

    @overload
    @classmethod
    def HtmlEncode(cls, string: str) -> str:
        """
        Converts a string to an HTML-encoded string.

        Args:
            string (str): Maximum length of 64,000 characters.

        Returns:
            str: converted string

        See Also:
            `HtmlEncode <http://www.access2base.com/access2base.html#HtmlEncode>`_
        """

    @overload
    @classmethod
    def HtmlEncode(cls, string: str, length: int) -> str:
        """
        Converts a string to an HTML-encoded string.

        Args:
            string (str): Maximum length of 64,000 characters.
            length (int): The output string will be truncated after length characters.
                However, an &-encoded character will remain complete.

        Returns:
            str: converted string

        See Also:
            `HtmlEncode <http://www.access2base.com/access2base.html#HtmlEncode>`_
        """

    @classmethod
    def OpenConnection(cls, thisdatabasedocument: Any = ...) -> Any:
        """
        Opens a connection to database.

        The invocation of the OpenConnection as a Sub is mandatory before any other use of the
        Access2Base API. It initializes the resources needed to process inside the API the
        subsequent invocations to its methods and actions.

        If the document is a Base document (suffix = ".odb") then a link is established with its database.

        If the document is not a Base document (a Writer, Calc, ... document), then a link is established
        with each database associated with the standalone forms contained in the document.

        Args:
            thisdatabasedocument (Any, optional): unknown

        Returns:
            Any: connecton.

        Note:
            If the access to the database requires a login and if not yet done, the user will be prompted
            for entering a username and a password.

            The syntax that was valid up to Access2Base version 1.0.0 is still accepted.
            However, the username and password arguments are ignored.

        See Also:
            `OpenConnection <http://www.access2base.com/access2base.html>`_
        """

    @classmethod
    def OpenDatabase(
            cls,
            connectionstring: str,
            username: str = ...,
            password: str = ...,
            readonly: bool = ...,
    ) -> _Database:
        """
        Opens Database.

        The OpenDatabase method returns a Database object that establishes a link with an external
        database represented by a database document (".odb" file).

        The returned object allows data retrieval and update in the targeted database.

        Args:
            connectionstring (str): Either the name under which the targeted database is registered
                or the URL of the ".odb" file referring to the targeted database.
            username (str, optional): user name if any.
            password (str, optional): user password if any.
            readonly (bool, optional): If True updates of the database data will be forbidden. Defaults to False.

        Returns:
            _Database: Database object.

        See Also:
            `OpenDatabase <http://www.access2base.com/access2base.html#OpenDatabase>`_
        """

    @classmethod
    def ProductCode(cls) -> str:
        """Gets product code such as: ``Access2Base x.y.z`` where x.y.z equals the version number of the library."""

    @classmethod
    def setValue(cls, shortcut: str, value: Any) -> bool:
        """
        Sets a property of an object designated by its shortcut notation.

        Args:
            shortcut (str): An object of types Form, Dialog or Control.
            value (Any): value to set.

        Returns:
            bool: True if success.

        See Also:
            `setValue <http://www.access2base.com/access2base.html#setValue>`_
        """

    SetValue = setValue

    @classmethod
    def SysCmd(cls, action: int, text: str = ..., value: int = ...) -> bool:
        """
        Manage progress meter in the status bar.

        The SysCmd method displays a progress meter or optional specified text in the status bar.
        By calling the SysCmd method with the various progress meter actions, you can display
        a progress meter in the status bar for an operation that has a known duration or
        number of steps, and update it to indicate the progress of the operation.

        Args:
            action (int): An acConstance.acSysCmd* value suca as acConstance.acSysCmdSetStatus
            text (str, optional): A string expression identifying the text to be displayed left-aligned
                in the status bar. This argument is required when the action argument is acSysCmdInitMeter,
                acSysCmdUpdateMeter, or acSysCmdSetStatus. This argument isn't valid for other action argument values.
            value (int, optional): A numeric expression that controls the display of the progress meter.
                This argument is required when the action argument is acSysCmdInitMeter.
                This argument isn't valid for other action argument values.

        Returns:
            bool: True if success.

        See Also:
            `SysCmd <http://www.access2base.com/access2base.html#SysCmd>`_
        """

    @overload
    @classmethod
    def TempVars(cls) -> _Collection:
        """
        Gets a collection represents the collection of TempVar objects.

        Returns:
            _Collection: A Collection object

        See Also:
            `TempVars <http://www.access2base.com/access2base.html#TempVars>`_
        """

    @overload
    @classmethod
    def TempVars(cls, var: int) -> _TempVar:
        """
        Gets a TempVar object.

        Args:
            var (int): The index-th item in the TempVars() collection.
                The 1st temporary var is TempVars(0), the 2nd is TempVars(1) and so on ...
                The last one is TempVars.Count - 1.

        Returns:
            _TempVar: A TempVar object corresponding to the index-th item in the TempVars() collection.

        See Also:
            `TempVars <http://www.access2base.com/access2base.html#TempVars>`_
        """

    @overload
    @classmethod
    def TempVars(cls, var: str) -> _TempVar:
        """
        Gets a TempVar object.

        Args:
            var (str): TempVar as a name.

        Returns:
            _TempVar: A TempVar object having the argument as name. The argument is NOT case-sensitive.

        See Also:
            `TempVars <http://www.access2base.com/access2base.html#TempVars>`_
        """

    @classmethod
    def Version(cls) -> str:
        """
        Gets either ``LibreOffice w.x.y.z`` or ``OpenOffice w.x.y.z`` where w.x.y.z is the version number.
        or the name and version of the database engine, f.i. ``HSQL Database Engine 1.8.0``.

        Returns:
            str: version
        """


class DoCmd(object, metaclass=_Singleton):
    """Collection of methods located in the DoCmd (Basic) module"""

    # W = _A2B.invokeWrapper
    basicmodule: Literal[-2]

    @classmethod
    def ApplyFilter(
            cls, filter: str = ..., sqlwhere: str = ..., controlname: str = ...
    ) -> bool:
        """
        Set filter on open table, query, form or subform.

        Use the ApplyFilter action to apply a filter, a query, or an SQL WHERE
        clause to a table, form, subform or query to restrict the records in the
        table or query, or the records from the underlying table or query of the form/subform.

        Args:
            filter (str, optional): The filter and sqlwhere arguments have identical meanings.
                They both contain a SQL Where clause without the word Where.
                If both arguments are present, the sqlwhere argument only is applied to the data.
            sqlwhere (str, optional): SQL WHERE clause.
            controlname (str, optional): The name of a subform of the active form.

        Returns:
            bool: True if success.

        See Also:
            `ApplyFilter <http://www.access2base.com/access2base.html#ApplyFilter>`_
        """

    @overload
    @classmethod
    def Close(cls, objecttype: int, objectname: str) -> bool:
        """
        Closes an object (table, query, form or report).

        Args:
            objecttype (int): The type of object to close.
            objectname (str): The name of the object to close. This argument is NOT case-sensitive.

        Returns:
            bool: True if success.

        Note:
            ``objecttype`` can be one of the following:

            - acConstants.acTable
            - acConstants.acQuery
            - acConstants.acForm
            - acConstants.acReport

        See Also:
            `Close <http://www.access2base.com/access2base.html#Close>`_
        """

    @overload
    @classmethod
    def Close(cls, objecttype: int, objectname: str, save: int) -> bool:
        """
        Closes an object (table, query, form or report).

        Args:
            objecttype (int): The type of object to close.
            objectname (str): The name of the object to close. This argument is NOT case-sensitive.
            save (int, optional): Indicates if a prompt to the user will prevent from closing without saving.
                acSavePrompt is the only supported value.

        Returns:
            bool: True if success.

        Note:
            ``objecttype`` can be one of the following:

            - acConstants.acTable
            - acConstants.acQuery
            - acConstants.acForm
            - acConstants.acReport

        See Also:
            `Close <http://www.access2base.com/access2base.html#Close>`_
        """

    @classmethod
    def CopyObject(
            cls,
            sourcedatabase: str,
            newname: str,
            sourceobjecttype: int,
            sourceobjectname: str,
    ) -> bool:
        """
        Copies tables and queries into identical (new) objects.

        The CopyObject action copies an existing query or table within the current database or
        from an external database to the current database.

        Args:
            sourcedatabase (str): The source database.
            newname (str): The name of the target copy.
            sourceobjecttype (int): The type of object to copy. acConstants.acTable or acConstants.acQuery.
            sourceobjectname (str): The name of the object to copy. This argument is NOT case-sensitive.

        Returns:
            bool: True if success.

        See Also:
            `CopyObject <http://www.access2base.com/access2base.html#CopyObject>`_
        """

    @classmethod
    def FindNext(cls) -> bool:
        """
        Gets the next instance of data that meets the criteria specified by the arguments of the last
        invoked FindRecord action.

        If a match has been found, the cursor is set in the matching field.
        Otherwise, it returns to the starting record.
        The starting record is NOT the record where the focus is on but the last record reached by
        the previous FindRecord action.

        Returns:
            bool: True if success.

        Notes:
            - A previous FindRecord action is mandatory. Otherwise, the invocation of FindNext will generate an error.
            - FindNext returns True if a matching occurrence has been found.

        See Also:
            `FindNext <http://www.access2base.com/access2base.html#FindNext>`_
        """

    @classmethod
    def FindRecord(
            cls,
            findwhat: Union[str, datetime.datetime, Number],
            match: int = ...,
            matchcase: bool = ...,
            search: int = ...,
            searchasformatted: bool = ...,
            onlycurrentfield: Union[int, str] = ...,
            findfirst: bool = ...,
    ) -> bool:
        """
        Gets the first instance of data that meets the criteria specified by the FindRecord arguments.

        This can be in a succeeding or prior record, or in the first record.
        The search is done in a single column or in all columns of a form (or subform)'s GridControl.
        If a match has been found, the cursor is set in the matching field.

        Args:
            findwhat (str | datetime | Number): Specifies the data you want to find in the record. Enter the text,
                number, or date you want to find.
            match (int, optional): Specifies where the data is located in the field.
                You can specify a search for data in any part of the field (acAnyWhere),
                for data that fills the entire field (acEntire), or for data located at the beginning of the
                field (acStart). Obviously this argument is meaningful only if FindWhat is a string.
                Can be acConstants.acAnywhere, acConstants.acEntire, or acConstants.acStart
                Defaults to acConstants.acEntire.
            matchcase (bool, optional): Specifies whether the search is case-sensitive
                (uppercase and lowercase letters must match exactly). Defaults to False.
            search (int, optional): Specifies whether the search proceeds from the current record up
                to the beginning of the records (acUp); down to the end of the records (acDown); or down
                to the end of the records and then from the beginning of the records to the current record,
                so all records are searched (acSearchAll).
                Can be acConstants.acDown, acConstants.acSearchAll or acConstants.acUp
                Defaults to acConstants.acSearchAll.
            searchasformatted (bool, optional): If present, must be False. True is not supported. Defaults to False.
            onlycurrentfield (int | str, optional): Specifies whether the search is confined to the current field in
                each record (acCurrent) or includes all fields in each record (acAll).
                Constants can be acConstants.acAll or acConstants.acCurrent.
                As string, the argument must contain a shortcut to a GridControl or to a column of a GridControl.
                Defaults to acConstants.acCurrent.
            findfirst (bool, optional): _description_. Defaults to True.

        Returns:
            bool: True if successful

        See Also:
            `FindRecord <http://www.access2base.com/access2base.html#FindRecord>`_
        """

    @overload
    @classmethod
    def GetHiddenAttribute(cls, objecttype: int) -> bool: ...

    @overload
    @classmethod
    def GetHiddenAttribute(cls, objecttype: int, objectname: str) -> bool:
        """
        Gets if a named window is currently hidden or visible.

        Args:
            objecttype (int): The type of object to hide or to show.
            objectname (str): The name of the object. This argument is NOT case-sensitive.
                The argument is mandatory when the ObjectType argument is one of next values:
                acTable, acQuery, acForm, acReport or acDocument.
                When the ObjectType is equal to acDocument, the ObjectName argument must contain the filename
                of the targeted window.

        Returns:
            bool: True if window is hidden; Otherwise, False.

        Note:
            **Arg** ``objecttype`` can be one of the following constants.

            - acConstants.acQuery
            - acConstants.acTable
            - acConstants.acForm
            - acConstants.acReport
            - acConstants.acDiagram
            - acConstants.acBasicIDE
            - acConstants.acDatabaseWindow
            - acConstants.acDocument

        See Also:
            `GetHiddenAttribute <http://www.access2base.com/access2base.html#GetHiddenAttribute>`_
        """

    @classmethod
    def GoToControl(cls, controlname: str) -> bool:
        """
        Set the focus on the named control on the active form.

        Args:
            controlname (str): The name of the control to move the focus to. This argument is NOT case-sensitive.

        Returns:
            bool: ``False`` if the control does not exist or is disabled; Otherwise, ``True``.

        See Also:
            `GoToControl <http://www.access2base.com/access2base.html#GoToControl>`_
        """

    @classmethod
    def GoToRecord(
            cls,
            objecttype: int = ...,
            objectname: str = ...,
            record: int = ...,
            offset: int = ...,
    ) -> bool:
        """
        Move to record indicated by ``record/offset`` in the window designated by ``objecttype`` and ``objectname``.

        Args:
            objecttype (int, optional): The type of object that contains the record you want to make current.
                Leave this argument blank to select the active window.
                Defaults to acConstants.acActiveDataObject.

            objectname (str, optional): The name of the object that contains the record you want to make the
                current record. If you leave the Object Type argument blank, leave this argument blank also.
                This argument may also contain a shortcut to a Form or a SubForm.

            record (int, optional): Specifies the record to make the current record.
                Defaults to acConstants.acNext.

            offset (int, optional): This argument specifies the record to make the current record.
                You can use the Offset argument in two ways.

                When the Record argument is acNext or acPrevious, the cursor moves the number of records forward or backward specified in the Offset argument.

                When the Record argument is acGoTo, the cursor moves to the record with the number equal to the Offset argument.
                Defaults to 1.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can be one of the following constants:

            - acConstants.acActiveDataObject
            - acConstants.acDataForm
            - acConstants.acDataTable
            - acConstants.acDataQuery

            **Arg** ``record`` can be one of the following constants:

            - acConstants.acFirst
            - acConstants.acGoTo
            - acConstants.acLast
            - acConstants.acNewRec
            - acConstants.acNext
            - acConstants.acPrevious

        See Also:
            `GoToRecord <http://www.access2base.com/access2base.html#GoToRecord>`_
        """

    @classmethod
    def Maximize(cls) -> bool:
        """
        Maximize the window having the focus.

        Returns:
            bool: True on success.
        """

    @classmethod
    def Minimize(cls) -> bool:
        """
        Minimize the window having the focus.

        Returns:
            bool: True on success.
        """

    @classmethod
    def MoveSize(
            cls, left: int = ..., top: int = ..., width: int = ..., height: int = ...
    ) -> bool:
        """
        Moves the active window to the coordinates specified by the argument values.

        Args:
            left (int, optional): The screen position for the left edge of the window relative to the left edge of the screen.
            top (int, optional): The screen position for the top edge of the window relative to the top edge of the screen.
            width (int, optional): The desired width of the window.
            height (int, optional): The desired height of the window.

        Returns:
            bool: True on success.

        See Also:
            `MoveSize <http://www.access2base.com/access2base.html#MoveSize>`_
        """

    @classmethod
    def OpenForm(
            cls,
            formname: str,
            view: int = ...,
            filter: str = ...,
            wherecondition: str = ...,
            datamode: int = ...,
            windowmode: int = ...,
            openargs: Any = ...,
    ) -> _Form:
        """
        Opens a form in Form view or in form Design view.

        You can select data entry and window modes for the form and restrict the records that the form displays.

        Args:
            formname (str): The name of the form to open.

            view (int, optional): The view in which the form will open.
                acNormal and acPreview are equivalent.
                Defaults to acNormal.

            filter (str, optional): A valid SQL WHERE clause (without the word WHERE).

            wherecondition (str, optional): A valid SQL WHERE clause (without the word WHERE).

            datamode (int, optional): Specifies if the user will be allowed to add new records acFormAdd,
                add new and edit existing records acFormEdit or only read existing records acFormReadOnly.
                acFormPropertySettings refers to the settings at form creation.
                Only acFormEdit allows record deletions.
                Defaults to acFormEdit.

            windowmode (int, optional): Mode. Defaults to acWindowNormal.

            openargs (any, optional): The argument is used to set the form's OpenArgs property.

        Returns:
            _Form: Form object.

        Note:
            **Arg** ``view`` can be one of the following constants.

            - acConstants.acDesign
            - acConstants.acNormal
            - acConstants.acPreview

            **Arg** ``datamode`` can be one of the following constants.

            - acConstants.acFormAdd
            - acConstants.acFormEdit
            - acConstants.acFormPropertySettings
            - acConstants.acFormReadOnly

            **Arg** ``windowmode`` can be one of the following constants.

            - acConstants.acHidden
            - acConstants.acWindowNormal

        See Also:
            `OpenForm <http://www.access2base.com/access2base.html#OpenForm>`_
        """

    @classmethod
    def OpenQuery(cls, queryname: str, view: int = ..., datamode: int = ...) -> bool:
        """
        Opens a query in normal view or in query design view.

        Args:
            queryname (str): The name of the query to open. This argument is NOT case-sensitive.

            view (int, optional): The view in which the query will open.
                acViewNormal and acViewPreview are equivalent.
                 Defaults to acNormal.

            datamode (int, optional): The user will be allowed to add new records and edit existing records.
                Defaults to acEdit.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``view`` can be one of the following constants.

            - acConstants.acDesign
            - acConstants.acNormal
            - acConstants.acPreview

        See Also:
            `OpenQuery <http://www.access2base.com/access2base.html#OpenQuery>`_
        """

    @overload
    @classmethod
    def OpenReport(cls, queryname: str) -> bool: ...

    @overload
    @classmethod
    def OpenReport(cls, queryname: str, view: int) -> bool:
        """
        Opens a report in normal view or in report design view.Query

        Args:
            queryname (str): The name of the report to open. This argument is NOT case-sensitive.
            view (int): The view in which the query will open.
                acViewNormal and acViewPreview are equivalent.
                Defaults to acNormal.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``view`` can be one of the following constants.

            - acConstants.acDesign
            - acConstants.acNormal
            - acConstants.acPreview

        See Also:
            `OpenReport <http://www.access2base.com/access2base.html#OpenReport>`_
        """

    @overload
    @classmethod
    def OpenSQL(cls, sql: str) -> bool: ...

    @overload
    @classmethod
    def OpenSQL(cls, sql: str, option: int) -> bool:
        """
        Opens a datasheet containing the data described by the provided SELECT SQL statement.

        Args:
            sql (str): A SELECT SQL statement.
            option (int, optional): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        Returns:
            bool: True if the execution of the SQL statement was successful.

        See Also:
            `OpenSQL <http://www.access2base.com/access2base.html#OpenSQL>`_
        """

    @classmethod
    def OpenTable(cls, tablename: str, view: int = ..., datamode: int = ...) -> bool:
        """
        Opens a table in normal view or in table design view.

        Args:
            tablename (str): The name of the table to open. This argument is NOT case-sensitive.

            view (int, optional): The view in which the table will open.
                acViewNormal and acViewPreview are equivalent
                Defaults to acNormal.

            datamode (int, optional): The user will be allowed to add new records and edit existing records.
                Defaults to acConstants.acEdit.

        Note:
            **Arg** ``view`` can be one of the following constants.

            - acConstants.acDesign
            - acConstants.acNormal
            - acConstants.acPreview

        Returns:
            bool: True on success.

        See Also:
            `OpenTable <http://www.access2base.com/access2base.html#OpenTable>`_
        """

    @classmethod
    def OutputTo(
            cls,
            objecttype: int,
            objectname: str = ...,
            outputformat: str = ...,
            outputfile: str = ...,
            autostart: bool = ...,
            templatefile: str = ...,
            encoding: int = ...,
            quality: int = ...,
    ) -> bool:
        """
        Outputs the data located in a specified form, table, or query.

        Args:
            objecttype (int): The type of object to output.

            objectname (str, optional): The valid name of an object of the type selected by the objecttype argument.
                If the objecttype is acOutputForm, and you want to output the active form, leave this argument blank.

            outputformat (str, optional): The output format, expressed as an acFormatXXX constant.
                If this argument is omitted, the user will be prompted for the output format.

            outputfile (str, optional): The full name, including the path, of the file you want to output the object to.
                If this argument is left blank, the user will be prompted for an output file name.

            autostart (bool, optional): If True, specifies that you want the appropriate application to start immediately
                after the OutputTo action runs, with the file specified by the outputfile argument opened.
                Defaults to False.

            templatefile (str, optional): Meaningful only if the objecttype argument is acOutputTable or
                acOutputQuery and the outputformat argument is HTML. Otherwise, must contain the null-length
                string. The full name, including the path, of the template file.

            encoding (int, optional): Meaningful only if the objecttype argument is acOutputTable or acOutputQuery.
                Defaults to acConstants.acUTF8Encoding.

            quality (int, optional): This argument is ignored. Defaults to acConstants.acExportQualityPrint.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can be one of the following constants:

            - acConstants.acOutputTable
            - acConstants.acOutputQuery
            - acConstants.acOutputForm

            **Arg** ``outputformat`` can be one of the following constants:

            - acConstants.acFormatPDF
            - acConstants.acFormatODT
            - acConstants.acFormatDOC
            - acConstants.acFormatHTML
            - acConstants.acFormatODS
            - acConstants.acFormatXLS
            - acConstants.acFormatXLSX
            - acConstants.acFormatTXT

        **Arg** ``quality`` can be one of the following constants:

            - acConstants.acExportQualityPrint
            - acConstants.acExportQualityScreen

        See Also:
            `OutputTo <http://www.access2base.com/access2base.html#OutputTo>`_
        """

    @classmethod
    def Quit(cls) -> Any:
        """
        The Quit action is not available from PYTHON scripts.

        Quits OpenOffice/LibreOffice Base. You can select one of several options for saving
        the database document before quitting.

        Returns:
            Any: unknown

        See Also:
            `Quit <http://www.access2base.com/access2base.html#Quit>`_
        """

    @classmethod
    def RunApp(cls, commandline: str) -> None:
        """
        Runs an external application given by its command line.

        The command line may be an executable file or a user file associated via its suffix with
        an executable application. Use caution when running executable files or code in macros or applications.
        Executable files or code can be used to carry out actions that might compromise the security of your
        computer and data.

        Args:
            commandline (str): The command line used to start the application
                (including the path and any other necessary parameters, such as switches that run
                the application in a particular mode).

        See Also:
            `RunApp <http://www.access2base.com/access2base.html#RunApp>`_
        """

    @classmethod
    def RunCommand(cls, command: Union[str, int]) -> bool:
        """
        Executes the command given as argument.

        Args:
            command (str | int): If numeric the Command is selected by using the VBA denomination.
                If the Type is a String, the LibO/AOO command-name is expected.

        Returns:
            bool: Always returns ``True``

        See Also:
            `RunCommand <http://www.access2base.com/access2base.html#RunCommand>`_
        """

    @overload
    @classmethod
    def RunSQL(cls, SQL: str) -> bool: ...

    @overload
    @classmethod
    def RunSQL(cls, SQL: str, option: int) -> bool:
        """
        Executes the SQL statement given as argument.

        The statement must execute an action.
        Typical statements are: INSERT INTO, DELETE, SELECT...INTO, UPDATE, CREATE TABLE, ALTER TABLE,
        DROP TABLE, CREATE INDEX, or DROP INDEX.

        Args:
            SQL (str): Specifies the statement to execute
            option (int): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        Returns:
            bool: True on success.

        See Also:
            `RunSQL <http://www.access2base.com/access2base.html#RunSQL>`_
        """

    @classmethod
    def SelectObject(
            cls, objecttype: int, objectname: str = ..., indatabasewindow: bool = ...
    ) -> bool:
        """
        Moves the focus to the specified window.

        Args:
            objecttype (int): The type of object to set the focus on.

            objectname (str, optional): The name of the object to set the focus on. This argument is NOT case-sensitive.
                The argument is mandatory when the objecttype argument is one of next values:
                acTable, acQuery, acForm, acReport or acDocument.
                When the ObjectType is equal to acDocument, the objectname argument must
                contain the filename of the window to be selected.

            indatabasewindow (bool, optional): Specifies if the object has to be selected in the Database Window.
                Must be False. Defaults to False.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can be one of the following constants.

            - acConstants.acTable
            - acConstants.acQuery
            - acConstants.acForm
            - acConstants.acReport
            - acConstants.acDiagram
            - acConstants.acDocument
            - acConstants.acBasicIDE
            - acConstants.acDatabaseWindow

        See Also:
            `SelectObject <http://www.access2base.com/access2base.html#SelectObject>`_
        """

    @classmethod
    def SendObject(
            cls,
            objecttype: int = ...,
            objectname: str = ...,
            outputformat: str = ...,
            to: str = ...,
            cc: str = ...,
            bcc: str = ...,
            subject: str = ...,
            messagetext: str = ...,
            editmessage: bool = ...,
            templatefile: str = ...,
    ) -> bool:
        """
        Outputs the data in the specified object (currently only a form) to several output formats and
        inserts it into an e-mail. Recipients, subject and other elements can be inserted automatically as well.

        Args:
            objecttype (int, optional): The type of object to output.
                Defaults to acConstants.acSendNoObject.

            objectname (str, optional): The valid name of an object of the type selected by the objecttype argument.
                If you want to output the active object, specify the object's type for the objecttype argument and
                leave this argument blank. If the objecttype argument is left empty or is equal to the default value,
                if this argument is not empty, then it will be interpreted as the full path name of the
                file to attach to the mail.

            outputformat (str, optional):The output format, expressed as an acFormatXXX constant.
                If this argument is omitted, the user will be prompted for the output format.

            to (str, optional): The recipients of the message whose names you want to put on the To line in the
                mail message. Separate the recipients' names you specify in this argument
                (and in the Cc and Bcc arguments) with a semicolon (;). If the mail application can't identify the
                recipients' names, the message isn't sent and an error occurs.

            cc (str, optional): The message recipients whose names you want to put on the
                Cc ("carbon copy") line in the mail message.

            bcc (str, optional): The message recipients whose names you want to put on the
                Bcc ("blind carbon copy") line in the mail message.

            subject (str, optional): The subject of the message. This text appears on the Subject line in the mail message.

            messagetext (str, optional): Any text you want to include in the message in addition to the database
                object or the attachment. This text appears in the main body of the mail message.
                If you leave this argument blank, no additional text is included in the mail message.
                If you leave the ObjectType and objectname arguments blank, you can use this argument to send
                a mail message without any database object.

            editmessage (bool, optional): Specifies whether the message can be edited before it's sent.
                If you select True, the electronic mail application starts automatically,
                and the message can be edited. If you select False, the message is sent without the
                user having a chance to edit the message. Defaults to True.

            templatefile (str, optional): If present, must be an empty string. Defaults to ''.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can one of the following constants:

            - acConstants.acSendNoObject
            - acConstants.acSendForm

            **Arg** ``outputformat`` can one of the following constants:

            - acConstants.acFormatPDF
            - acConstants.acFormatODT
            - acConstants.acFormatDOC
            - acConstants.acFormatHTML

        See Also:
            `SendObject <http://www.access2base.com/access2base.html#SendObject>`_
        """

    @classmethod
    def SetHiddenAttribute(
            cls, objecttype: int, objectname: str = ..., hidden: bool = ...
    ) -> bool:
        """
        Hides or shows the specified window.

        Args:
            objecttype (int): The type of object to hide or show.

            objectname (str, optional): The name of the object to hide or to show. This argument is NOT case-sensitive.
                The argument is mandatory when the objecttype argument is one of next values:
                acTable, acQuery, acForm, acReport or acDocument.
                When the objecttype is equal to acDocument, the objectname argument must
                contain the filename of the targeted window.

            hidden (bool, optional): True hides the object window.
                False makes the object visible again and sets the focus on the window. Defaults to True.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can one of the following constants:

            - acConstants.acTable
            - acConstants.acQuery
            - acConstants.acForm
            - acConstants.acReport
            - acConstants.acDiagram
            - acConstants.acBasicIDE
            - acConstants.acDatabaseWindow
            - acConstants.acDocument

        See Also:
            `SetHiddenAttribute <http://www.access2base.com/access2base.html#SetHiddenAttribute>`_
        """

    @classmethod
    def SetOrderBy(cls, orderby: str = ..., controlname: str = ...) -> bool:
        """
        Sort ann open table, query, form or subform (if pvControlName present)

        Sort is applied to the table, form or datasheet (for example, query result) that is active and has the focus.

        Args:
            orderby (str, optional): The name of the field or fields on which you want to sort records.
                When you use more than one field name, separate the names with a comma (,).
            controlname (str, optional): The name of a subform of the active form.

        Returns:
            bool: True on success.

        See Also:
            `SetOrderBy <http://www.access2base.com/access2base.html#SetOrderBy>`_
        """

    @classmethod
    def ShowAllRecords(cls) -> bool:
        """
        Removes any existing filters and sorts that may exist on the current table, query, or form.

         Returns:
            bool: True on success.
        """


class Basic(object, metaclass=_Singleton):
    """Collection of helper functions having the same behaviour as their Basic counterparts"""

    @classmethod
    def ConvertFromUrl(cls, url: str) -> str:
        """
        Convert from url

        Args:
            url (str): a string representing a file in URL format

        Returns:
            str: The same file name in native operating system notation

        Example:
            .. code::

                a = bas.ConvertFromUrl('file:////boot.sys')
        """

    @classmethod
    def ConvertToUrl(cls, file):
        """
        Convert to url

        Args:
            file (str): a string representing a file in native operating system notation

        Returns:
            str: The same file name in URL format

        Exampe:
            .. code::

                >>> a = bas.ConvertToUrl('C:\\boot.sys')
                >>> print(a)
                'file:///C:/boot.sys'
        """

    @classmethod
    def CreateUnoService(cls, servicename: str) -> UnoXInterface:
        """
        Creates a uno service

        Args:
            servicename (str):  a string representing the service to creat

        Returns:
            XInterface: A UNO object

        Example:
            .. code::

                a = bas.CreateUnoService('com.sun.star.i18n.CharacterClassification')
        """

    @classmethod
    def DateAdd(
            cls,
            add: Any,
            count: int,
            datearg: Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time]
    ) -> datetime.datetime:
        """
        Adds a date or time interval to a given date/time a number of times and returns the resulting date.

        Args:
            add (Any): A string expression from the following table, specifying the date or time interval.
            count (int): A numerical expression specifying how often the interval value will be added when
                positive or subtracted when negative.
            datearg (Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time]): A given
                datetime.datetime value, the interval value will be added number times to this datetime.datetime value.

        Returns:
            datetime.datetime: A datetime.datetime value.
        """

    @classmethod
    def DateDiff(
            cls,
            add: str,
            date1: Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time],
            date2: Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time],
            weekstart: int = ...,
            yearstart: int = ...,
    ) -> int:
        """
        Returns the number of date or time intervals between two given date/time values.

        Args:
            add (Any): A string expression specifying the date interval, as detailed in above DateAdd method.
            date1 (Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time]): The frist
            datetime.datetime values to be compared.
            date2 (Union[float, time.struct_time, datetime.datetime, datetime.date, datetime.time]): The second
            datetime.datetime values to be compared.
            weekstart (int, optional): An optional parameter that specifies the starting day of a week.
            yearstart (int, optional): An optional parameter that specifies the starting week of a year.

        Note:
            **Arg** ``weekstart`` values::

                0 - Use system default value
                1 - Sunday (default)
                2 - Monday
                3 - Tuesday
                4 - Wednesday
                5 - Thursday
                6 - Friday
                7 - Saturday

            **Arg** ``yearstart`` values::

                0 - Use system default value
                1 - Week 1 is the week with January, 1st (default)
                2 - Week 1 is the first week containing four or more days of that year
                3 - Week 1 is the first week containing only days of the new year

       Returns:
           int: A Number
       """

    @classmethod
    def DatePart(
            cls,
            add: str,
            datearg: Union[time.struct_time, datetime.datetime, datetime.date, datetime.time, str],
            weekstart: int = ...,
            yearstart: int = ...,
    ) -> int:
        """
        Gets a specified part of a date.

        Args:
            add (str): A string expression specifying the date interval, as detailed in above DateAdd method.
            datearg (Union[time.struct_time, datetime.datetime, datetime.date, datetime.time, str]): The date/time
                from which the result is calculated.
            weekstart (int, optional): An optional parameter that specifies the starting day of a week.
            yearstart (int, optional): An optional parameter that specifies the starting week of a year.

        Note:
            **Arg** ``weekstart`` values::

                0 - Use system default value
                1 - Sunday (default)
                2 - Monday
                3 - Tuesday
                4 - Wednesday
                5 - Thursday
                6 - Friday
                7 - Saturday

            **Arg** ``yearstart`` values::

                0 - Use system default value
                1 - Week 1 is the week with January, 1st (default)
                2 - Week 1 is the first week containing four or more days of that year
                3 - Week 1 is the first week containing only days of the new year

        Returns:
            int: The extracted part for the given date/time.
        """

    @classmethod
    def DateValue(cls, datestring: str) -> datetime.datetime:
        """
        Convenient function to replicate VBA DateValue()

        Args:
            datestring (str): a date as a string

        Returns:
            datetime.datetime: The computed date.

        Example:
            .. code::

                >>> a = Basic.DateValue('2021-02-18')
                >>> print(a)
                datetime.datetime(2021, 2, 18, 0, 0)
        """

    @classmethod
    def Format(cls, value: Any, format: str = ...) -> str:
        """
        Formats a string

        Args:
            value (Any): a date or a number
            format (str, optional): the format to apply. Defaults to "".

        Returns:
            str: The formatted value

        Example:
            .. code::

                >>> a =  Basic.Format(6328.2, '##,##0.00')
                >>> print(a)
                '6,328.20'

        See Also:
            `Format <https://tinyurl.com/ycv7q52r#Format>`_
        """

    @classmethod
    def GetGuiType(cls) -> int:
        """
        Gets gui type

        Returns:
            int: The GetGuiType value, 1 for Windows, 4 for UNIX

        Example:
            .. code::

                >>> print(Basic.GetGuiType())
                1
        """

    @staticmethod
    def GetPathSeparator() -> str: ...

    @classmethod
    def GetSystemTicks(cls) -> int:
        """
        Convenient function to replicate VBA GetSystemTicks()

        Returns:
            int: _description_
        """

    @classmethod
    def MsgBox(cls, text: str, type: int = ..., dialogtitle: str = ...) -> int:
        """
        Displays a dialogue box containing a message and returns a value.

        Convenient function to replicate VBA MsgBox()

        Args:
            text (str): String expression displayed as a message in the dialog box.
            type (int, optional):Any integer expression that specifies the dialog type, as well as the number and
                type of buttons to display, and the icon type. buttons represents a combination of bit patterns,
                that is, a combination of elements can be defined by adding their respective values.
            dialogtitle (str, optional): String expression displayed in the title bar of the dialog. Defaults to "".

        Returns:
            int: The pressed button as int.

        Example:
            .. code::

                >>> a = Basic.MsgBox("Las Vegas", acConstants.vbDefaultButton2 + acConstants.vbCritical + acConstants.vbAbortRetryIgnore, "Dialog title")
                >>> print(a)
                4 # depends on button that was clicked. 3, 4 or 5
        """

    class GlobalScope(object, metaclass=_Singleton):
        @classmethod  # Mandatory because the GlobalScope class is normally not instantiated
        def BasicLibraries(cls) -> Any: ...

        @classmethod
        def DialogLibraries(cls) -> Any: ...

    @classmethod
    def InputBox(
            cls,
            text: str,
            title: str = ...,
            default: str = ...,
            xpos: int = ...,
            ypos: int = ...,
    ) -> str:
        """
        Displays an input box.

        Args:
            text (str): String expression displayed as the message in the dialog box.
            title (str, optional): String expression displayed in the title bar of the dialog box.
            default (str, optional): String expression displayed in the text box as default if no other input is given.
            xpos (int, optional): Integer expression that specifies the horizontal position of the dialog.
                The position is an absolute coordinate and does not refer to the window of LibreOffice.
            ypos (int, optional): Integer expression that specifies the vertical position of the dialog.
                The position is an absolute coordinate and does not refer to the window of LibreOffice.
                If xpos and ypos are omitted, the dialog is centered on the screen.
                The position is specified in twips.

        Returns:
            str: _description_

        See Also:
            `Twips <https://tinyurl.com/yynxq84w#twips>`_
        """

    @classmethod
    def Now(cls) -> datetime.datetime:
        """
        Returns the current system date and time as a datetime.datetime Python native object.

        Returns:
            datetime.datetime: datetime.
        """

    @classmethod
    def RGB(cls, red: int, green: int, blue: int) -> int:
        """
        Returns an integer color value consisting of red, green, and blue components.

        Args:
            red (int): Any integer expression that represents the red component (0-255) of the composite color.
            green (int): Any integer expression that represents the green component (0-255) of the composite color.
            blue (int): Any integer expression that represents the blue component (0-255) of the composite color.

        Returns:
            int: Integer representing rgb color.
        """

    @classmethod
    def Timer(cls) -> int: ...

    @staticmethod
    def Xray(myObject: Any) -> None:
        """
        Inspect Uno objects or variables.

        Args:
            myObject (Any): A variable or UNO object.
        """


class _BasicObject(object):
    """
    Parent class of Basic objects
    Each subclass is identified by its classProperties:
         dictionary with keys = allowed properties, value = True if editable or False
    Each instance is identified by its
        - reference in the cache managed by Basic
        - type ('DATABASE', 'COLLECTION', ...)
        - name (form, control, ... name) - may be blank
    Properties are got and set following next strategy:
        1. Property names are controlled strictly ('Value' and not 'value')
        2. Getting a property value for the first time is always done via a Basic call
        3. Next occurrences are fetched from the Python dictionary of the instance if the property is read-only, otherwise via a Basic call
        4. Methods output might force the deletion of a property from the dictionary ('MoveNext' changes 'BOF' and 'EOF' properties)
        5. Setting a property value is done via a Basic call, except if self.internal == True
    """

    def __init__(
            self, reference: int = ..., objtype: Any = ..., name: str = ...
    ) -> None: ...

    def __getattr__(self, name: str) -> Any: ...

    def __setattr__(self, name: str, value: Any) -> None: ...

    def __repr__(self) -> str: ...

    def _Reset(self, propertyname: str, basicreturn: Union[int, Any] = ...) -> Any:
        """force new value or erase properties from dictionary (done to optimize calls to Basic scripts)"""

    @property
    def Name(self) -> str: ...

    @property
    def ObjectType(self) -> str: ...

    def Dispose(self) -> Any: ...

    def getProperty(self, propertyname: str, index: Union[int, str] = ...) -> Any: ...

    GetProperty = getProperty

    def hasProperty(self, propertyname: str) -> bool: ...

    HasProperty = hasProperty

    def Properties(self, index: Union[int, str] = ...) -> Any: ...

    def setProperty(
            self, propertyname: str, value: Any, index: Union[int, str] = ...
    ) -> None: ...

    SetProperty = setProperty


class _Collection(_BasicObject):
    """Collection object built as a Python iterator"""

    def __init__(self, reference: int = ..., objtype: Any = ...) -> None: ...

    def __iter__(self) -> Self: ...

    def __next__(self) -> Any: ...

    def __len__(self) -> int: ...

    def Add(self, table: _BasicObject, value: Any = ...) -> bool: ...

    def Delete(self, name: str) -> bool: ...

    def Item(self, index: int) -> Any: ...

    def Remove(self, tempvarname: str) -> bool: ...

    def RemoveAll(self) -> bool: ...

    @property
    def Count(self) -> int: ...


class _CommandBar(_BasicObject):
    """
    CommandBar object describes a toolbar, the menubar or the statusbar.

    See Also:
        `CommandBar <http://www.access2base.com/access2base.html#CommandBar>`_
    """

    ObjectType: Literal["COMMANDBAR"]

    @overload
    def CommandBarControls(self) -> _Collection:
        """Return a Collection type"""

    @overload
    def CommandBarControls(self, index: Union[int, str]) -> _CommandBarControl:
        """Return an object of type CommandBarControl indicated by its index"""

    def Reset(self) -> bool:
        """Reset a whole command bar to its initial values"""

    @property
    def BuiltIn(self) -> bool:
        """
        Gets ``True`` if the specified command bar control is a built-in control of the container CommandBar.
        """

    @property
    def Visible(self) -> bool:
        """
        Gets/Sets the visible/hidden status of the CommandBarControl.
        """


class _CommandBarControl(_BasicObject):
    """
    CommandBarControl object is a member of the CommandBarControls collection related to the CommandBar object.

    See Also:
        `CommandBarControl <http://www.access2base.com/access2base.html#CommandBarControl>`_
    """

    ObjectType: Literal["COMMANDBARCONTROL"]

    def Execute(self) -> Any:
        """Execute the command stored in a toolbar button"""

    @property
    def BeginGroup(self) -> bool:
        """
        Gets ``True`` if the specified command bar control appears at the beginning of a group of controls on the command bar.
        """

    @property
    def BuiltIn(self) -> bool:
        """
        Gets ``True`` if the specified command bar control is a built-in control of the container CommandBar.
        """

    @property
    def Caption(self) -> str:
        """
        Gets the caption text for a command bar control.
        """

    @property
    def Index(self) -> int:
        """
        Gets an Integer representing the index number for a CommandBarControl object in the collection.
        """

    @property
    def OnAction(self) -> str:
        """
        Gets/Sets the name of a command or a Basic procedure that will run when the user clicks the CommandBarControl.
        """

    @property
    def Parent(self) -> Any:
        """
        Gets the Parent object for the CommandBarControl object.
        """

    @property
    def TooltipText(self) -> str:
        """
        Gets/Sets the text displayed in a CommandBarControl's ScreenTip.
        """

    @property
    def Type(self) -> int:
        """
        Gets msoControlButton (=1).
        """

    @property
    def Visible(self) -> bool:
        """
        Gets/Sets the visible/hidden status of the CommandBarControl.
        """


class _Control(_BasicObject):
    ObjectType: Literal["CONTROL"]

    # region properties
    @property
    def BackColor(self) -> int:
        """
        Gets/Sets the color of the interior of a control.
        """

    @property
    def BorderColor(self) -> int:
        """
        Gets/Sets the color of a control's border.
        """

    @property
    def BorderStyle(self) -> UnoLineStyle:
        """
        Gets/Sets how a control's border appears.

        Returns:
            LineStyle: LineStyle

        See Also:
            `LibreOffice API LineStyle <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1drawing.html#a86e0f5648542856159bb40775c854aa7>`_
        """

    @property
    def Cancel(self) -> bool:
        """
        Gets/Sets whether a command button is also the Cancel button on a form.
        """

    @property
    def Caption(self) -> str:
        """
        Gets/Sets the label associated with a control.
        If the control is located within a GridControl, the Caption specifies the column heading.
        """

    @property
    def ControlSource(self) -> Any:
        """
        The ControlSource property specifies the database field bound to the Control.
        """

    @property
    def ControlTipText(self) -> str:
        """
        Gets/Sets the text that appears in a ScreenTip when you hold the mouse pointer over a control.
        """

    @property
    def ControlType(self) -> int:
        """
        Gets the type of a control.
        """

    @property
    def Default(self) -> bool:
        """
        Gets/Sets whether a CommandButton is the default button on a form.
        """

    @property
    def DefaultValue(self) -> Any:
        """
        Gets/Sets a value that is automatically entered in a field when a new record is created.
        """

    @property
    def Enabled(self) -> bool:
        """
        Gets/Sets if the cursor can access the control.
        """

    @property
    def FontBold(self) -> bool:
        """
        Gets/Sets Font Bold state.
        """

    @property
    def FontItalic(self) -> bool:
        """
        Gets/Sets Font Italic state.
        """

    @property
    def FontName(self) -> str:
        """
        Gets/Sets Font Name.
        """

    @property
    def FontSize(self) -> int:
        """
        Gets/Sets Font Size.
        """

    @property
    def FontUnderline(self) -> bool:
        """
        Gets/Sets Font Underline state.
        """

    @property
    def FontWeight(self) -> float:
        """
        Gets/Sets Font Weight.
        """

    @property
    def ForeColor(self) -> int:
        """
        Gets/Sets Fore Color.
        """

    @property
    def Form(self) -> _SubForm:
        """
        Gets the SubForm object corresponding with the SubForm control.
        """

    @property
    def Format(self) -> str:
        """
        Gets/Sets the way numbers, dates, times, and text are displayed
        """

    @property
    def ItemData(self) -> Any:
        """
        Gets the data for the specified row in a ComboBox or a ListBox.
        """

    @property
    def ListCount(self) -> int:
        """
        Gets the number of rows in a ListBox or the list box portion of a ComboBox.
        """

    @property
    def ListIndex(self) -> int:
        """
        Gets/Sets which item is selected in a ListBox or a ComboBox.
        """

    @property
    def Locked(self) -> bool:
        """
        Gets/Sets whether you can edit data in a control.
        """

    @property
    def MultiSelect(self) -> bool:
        """
        Gets/Sets whether a user can make multiple selections in a ListBox on a form.
        """

    @property
    def OnActionPerformed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveAction(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveReset(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveUpdate(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnErrorOccurred(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnFocusGained(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnFocusLost(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnItemStateChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnKeyPressed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnKeyReleased(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseDragged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseEntered(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseExited(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseMoved(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMousePressed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseReleased(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnResetted(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnTextChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnUpdated(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OptionValue(self) -> str:
        """
        Gets the value that is stored in the database when a RadioButton is selected and the record saved.
        """

    @property
    def Page(self) -> int:
        """
        Gets/Sets the page on which the control is visible.
        """

    @property
    def Parent(self) -> Any:
        """
        Gets the parent object of the control.
        """

    @property
    def Picture(self) -> str:
        """
        Gets/Sets the image to be displayed in an ImageControl or ImageButton control.
        """

    @property
    def Required(self) -> bool:
        """
        Gets/Sets whether a control must contain a value when the record is edited.
        """

    @property
    def RowSource(self) -> Any:
        """
        Gets/Sets the source of the data in a ListBox or a ComboBox.
        """

    @property
    def RowSourceType(self) -> uno.Enum:
        """
        Gets/Sets the source (tablename, queryname or SQL statement) of the data in a ListBox or a ComboBox.

        Returns:
            uno.Enum: ListSourceType

        See Also:
            `LibreOffice API ListSourceType <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1form.html#a52e06ed91fb133bc98c089a401a724fb>`_

        Example:
            .. code::

                >>> from com.sun.star.form.ListSourceType import TABLE as ST_TABLE
                >>> instance.RowSourceType = ST_TABLE
        """

    @property
    def Selected(self) -> bool:
        """
        Gets/Sets if an item in the data proposed by a ListBox is currently selected.
        """

    @property
    def SelLength(self) -> int: ...

    @property
    def SelStart(self) -> int: ...

    @property
    def SelText(self) -> str: ...

    @property
    def SubType(self) -> str:
        """
        Gets the type of a control.
        """

    @property
    def TabIndex(self) -> int:
        """
        Gets/Sets a control's place in the tab order on a form.
        """

    @property
    def TabStop(self) -> bool:
        """
        Gets/Sets whether you can use the TAB key to move the focus to a control.
        """

    @property
    def Tag(self) -> str:
        """
        Gets/Sets extra information about a control.
        """

    @property
    def Text(self) -> str:
        """
        Gets/Sets the text contained in a text box (or similar).
        """

    @property
    def TextAlign(self) -> int:
        """
        Gets/Sets the alignment of the text in a control.

        See Also:
            `LibreOffice API TextAlign <https://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1awt_1_1TextAlign.html>`_

        Example:
            .. code::

                >>> from com.sun.star.awt.TextAlign import CENTER
                >>> instance.TextAlign = CENTER
        """

    @property
    def TripleState(self) -> bool:
        """
        Gets/Sets how a CheckBox wll display Null values.
        """

    @property
    def Value(self) -> Any:
        """
        Gets/Sets the value contained in a control.
        """

    @property
    def Visible(self) -> bool:
        """
        Gets/Sets if a control is visible or hidden.
        """

    @property
    def BoundField(self) -> UnoColumn: ...

    @property
    def ControlModel(self) -> XControlModel: ...

    @property
    def ControlView(self) -> Union[XControl, None]: ...

    @property
    def LabelControl(self) -> Union[FixedText, GroupBox]: ...

    # endregion properties

    # region Methods
    @overload
    def AddItem(self, value: Any) -> bool: ...

    @overload
    def AddItem(self, value: Any, index: int) -> bool:
        """Add an item in a Listbox"""

    @overload
    def Controls(self) -> _Collection: ...

    @overload
    def Controls(self, index: Union[str, int]) -> _Control: ...

    # Overrides method in parent class: list of properties is strongly control type dependent
    def hasProperty(self, propertyname: str) -> bool: ...

    HasProperty = hasProperty

    def RemoveItem(self, index: Union[str, int]) -> bool:
        """
        Remove an item from a Listbox

        Returns:
            bool: True on success.
        """

    def Requery(self) -> bool:
        """Refresh data displayed in a form, subform, combobox or listbox"""

    def SetSelected(self, value: Any, index: int) -> bool:
        """Workaround for limitation of Basic: Property Let does not accept optional arguments"""

    def SetFocus(self) -> bool:
        """Execute setFocus method"""
    # endregion Methods


class _Database(_BasicObject):
    ObjectType: Literal["DATABASE"]

    # region Properties
    @property
    def Connect(self) -> str:
        """
        Gets the connection string as displayed on the statusbar.
        """

    @property
    def Connection(self) -> XConnection: ...

    @property
    def Document(self) -> OfficeDatabaseDocument: ...

    @property
    def MetaData(self) -> XDatabaseMetaData: ...

    @property
    def OnCreate(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnFocus(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnLoad(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnLoadFinished(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnModifyChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnNew(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnPrepareUnload(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnPrepareViewClosing(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSave(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSaveAs(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSaveAsDone(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSaveAsFailed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSaveDone(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSaveFailed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSubComponentClosed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnSubComponentOpened(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnTitleChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnUnfocus(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnUnload(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnViewClosed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnViewCreated(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def Version(self) -> str:
        """Something like 'HSQL Database Engine 1.8.0'"""

    # endregion Properties

    # region Methods
    def Close(self) -> bool:
        """
        Close the database object.

        Returns:
            bool: True on success.
        """

    def CloseAllRecordsets(self) -> None:
        """Housekeeping of eventual open recordsets"""

    @overload
    def CreateQueryDef(self, name: str, sqltext: str) -> _QueryDef: ...

    @overload
    def CreateQueryDef(self, name: str, sqltext: str, option: int) -> _QueryDef:
        """
        Gets a QueryDef object based on SQL statement.

        Args:
            name (str): The name of the new query,
            sqltext (str): The SQL statement to be executed when the query if fired.
            option (int): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        Returns:
            _QueryDef: QueryDef object.

        See Also:
            `CreateQueryDef <http://www.access2base.com/access2base.html#CreateQueryDef>`_
        """

    def CreateTableDef(self, name: str) -> _TableDef:
        """
        Creates a new TableDef object in the current database.

        This method offers the capacity to create from the Basic code a new table
        independently of the underlying RDBMS. Thus, without using SQL.
        However only a limited set of options are available for field descriptions.

        Args:
            name (str): The name of the new table.

        Returns:
            _TableDef: TableDef object.

        See Also:
            `CreateTableDef <http://www.access2base.com/access2base.html#CreateTableDef>`_
        """

    @overload
    def DAvg(self, expression: str, domain: str) -> Union[float, None]: ...
    @overload
    def DAvg(self, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the average of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DAvg
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DAvg function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The average of a set of values in a specified set of records (a domain).
                If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DAvg <http://www.access2base.com/access2base.html#DAvg>`_
        """

    @overload
    def DCount(self, expression: str, domain: str) -> Union[int, None]: ...

    @overload
    def DCount(self, expression: str, domain: str, criteria: str) -> Union[int, None]:
        """
        Gets the number of records that are in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DCount
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DCount function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            int | None: the number of records that are in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DCount <http://www.access2base.com/access2base.html#DCount>`_
        """

    def DLookup(
            self, expression: str, domain: str, criteria: str = ..., orderclause: str = ...
    ) -> Any:
        """
         Gets the value of a particular field from a specified set of records (a domain).

         You can use the DLookup function to display the value of a field that isn't in the record
         source for your form. For example, suppose you have a form based on an Order Details table.
         The form displays the OrderID, ProductID, UnitPrice, Quantity, and Discount fields.
         However, the ProductName field is in another table, the Products table.
         You could use the DLookup function in an event to display the ProductName on the same form.

        Args:
           expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DLookup
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DLookup function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.
            orderclause (str, optional): A string expression specifying the sequence of the returned records.
                It is a SQL ORDER BY clause without the words ORDER BY. It can include the ASC or DESC keywords.

        Returns:
            Any: result

        See Also:
            `DLookup <http://www.access2base.com/access2base.html#DLookup>`_
        """

    @overload
    def DMax(self, expression: str, domain: str) -> Union[float, None]: ...

    @overload
    def DMax(self, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the maximum value of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DMax
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DMax function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: the maximum value of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DMax <http://www.access2base.com/access2base.html#%5B%5BDMin%2C%20DMax%5D%5D>`_
        """

    @overload
    def DMin(self, expression: str, domain: str) -> Union[float, None]: ...

    @overload
    def DMin(self, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the minimum value of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DMin
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DMin function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: the minimum value of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DMin <http://www.access2base.com/access2base.html#%5B%5BDMin%2C%20DMax%5D%5D>`_
        """

    @overload
    def DStDev(self, expression: str, domain: str) -> Union[float, None]: ...

    @overload
    def DStDev(self, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the standard deviation of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DStDev
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DStDev function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The standard deviation of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DStDev <http://www.access2base.com/access2base.html#%5B%5BDStDev%2C%20DStDevP%5D%5D>`_
        """

    @overload
    def DStDevP(self, expression: str, domain: str) -> Union[float, None]: ...

    @overload
    def DStDevP(self, expression: str, domain: str, criteria: str) -> Union[float, None]:
        """
        Gets the standard deviation of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DStDevP
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DStDevP function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            float | None: The standard deviation of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DStDevP <http://www.access2base.com/access2base.html#%5B%5BDStDev%2C%20DStDevP%5D%5D>`_
        """

    @overload
    def DVar(self, expression: str, domain: str) -> Union[Any, None]: ...

    @overload
    def DVar(self, expression: str, domain: str, criteria: str) -> Union[Any, None]:
        """
        Gets the variance of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DVar
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DVar function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            Any | None: the variance of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DVar <http://www.access2base.com/access2base.html#%5B%5BDVar%2C%20DVarP%5D%5D>`_
        """

    @overload
    def DVarP(self, expression: str, domain: str) -> Union[Any, None]: ...

    @overload
    def DVarP(self, expression: str, domain: str, criteria: str) -> Union[Any, None]:
        """
        Gets the variance of a set of values in a specified set of records (a domain).

        Args:
            expression (str): An expression that identifies the field whose value you want to return.
                It can be a string expression identifying a field in a table or query,
                or it can be a SQL expression that performs a calculation on data in that field.
                However, the SQL expression must not include any SQL aggregate function.
            domain (str): A string expression identifying the set of records that constitutes the domain.
                It can be a table name or a query name for a query that does not require a parameter.
            criteria (str): A string expression used to restrict the range of data on which the DVarP
                function is performed. For example, criteria is often equivalent to the WHERE
                clause in an SQL expression, without the word WHERE. If criteria is omitted,
                the DVarP function evaluates expr against the entire domain. Any field that is included
                in criteria must also be a field in domain.

        Returns:
            Any | None: the variance of a set of values in a specified set of records (a domain).
            If no record satisfies criteria or if domain contains no records then None is returned.

        See Also:
            `DVarP <http://www.access2base.com/access2base.html#%5B%5BDVar%2C%20DVarP%5D%5D>`_
        """

    def OpenRecordset(
            self, source: str, type: int = ..., option: int = ..., lockedit: int = ...
    ) -> _Recordset:
        """
        Gets a new Recordset object and appends it to the Recordsets collection of the concerned database object.

        Args:
            source (str): A table name, a query name, or an SQL statement that returns records
            type (int, optional): If the argument is present its only allowed value is acConstants.dbOpenForwardOnly.
                Forces one-directional browsing of the records.
            option (int, optional): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.
            lockedit (int, optional): 	If the argument is present its only allowed value is acConstants.dbReadOnly.
                Forces dirty read and prevents from database updates.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `OpenRecordset <http://www.access2base.com/access2base.html#OpenRecordset>`_
        """

    @overload
    def OpenSQL(self, SQL: str) -> bool: ...

    @overload
    def OpenSQL(self, SQL: str, option: int) -> bool:
        """
        Opens a datasheet containing the data described by the provided SELECT SQL statement.

        Args:
            SQL (str): A SELECT SQL statement.
            option (int): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        Returns:
            bool: True on success.

        See Also:
            `OpenSQL <http://www.access2base.com/access2base.html#OpenSQL>`_
        """

    def OutputTo(
            self,
            objecttype: int,
            objectname: str = ...,
            outputformat: str = ...,
            outputfile: str = ...,
            autostart: bool = ...,
            templatefile: str = ...,
            encoding: int = ...,
            quality: int = ...,
    ) -> bool:
        """
        Outputs the data located in a specified form, table, or query.

        Args:
            objecttype (int): The type of object to output.

            objectname (str, optional): The valid name of an object of the type selected by the objecttype argument.
                If the objecttype is acOutputForm, and you want to output the active form, leave this argument blank.

            outputformat (str, optional): The output format, expressed as an acFormatXXX constant.
                If this argument is omitted, the user will be prompted for the output format.

            outputfile (str, optional): The full name, including the path, of the file you want to output the object to.
                If this argument is left blank, the user will be prompted for an output file name.

            autostart (bool, optional): If True, specifies that you want the appropriate application to start immediately
                after the OutputTo action runs, with the file specified by the outputfile argument opened.
                Defaults to False.

            templatefile (str, optional): Meaningful only if the objecttype argument is acOutputTable or
                acOutputQuery and the outputformat argument is HTML. Otherwise, must contain the null-length
                string. The full name, including the path, of the template file.

            encoding (int, optional): Meaningful only if the objecttype argument is acOutputTable or acOutputQuery.
                Defaults to acConstants.acUTF8Encoding.

            quality (int, optional): This argument is ignored. Defaults to acConstants.acExportQualityPrint.

        Returns:
            bool: True on success.

        Note:
            **Arg** ``objecttype`` can be one of the following constants:

            - acConstants.acOutputTable
            - acConstants.acOutputQuery
            - acConstants.acOutputForm

            **Arg** ``outputformat`` can be one of the following constants:

            - acConstants.acFormatPDF
            - acConstants.acFormatODT
            - acConstants.acFormatDOC
            - acConstants.acFormatHTML
            - acConstants.acFormatODS
            - acConstants.acFormatXLS
            - acConstants.acFormatXLSX
            - acConstants.acFormatTXT

        **Arg** ``quality`` can be one of the following constants:

            - acConstants.acExportQualityPrint
            - acConstants.acExportQualityScreen

        See Also:
            `OutputTo <http://www.access2base.com/access2base.html#OutputTo>`_
        """

    @overload
    def QueryDefs(self) -> _Collection:
        """
        Gets instances of all queries present in the current database.

        Returns:
            _Collection: A Collection object.

        See Also:
            `QueryDefs <http://www.access2base.com/access2base.html#QueryDefs>`_
        """

    @overload
    def QueryDefs(self, index: int) -> _QueryDef:
        """
        Gets an instance of a query present in the current databse.

        Args:
            index (int): A QueryDef object corresponding to the index-th item in the QueryDefs() collection.

        Returns:
            _QueryDef: QueryDef object.

        See Also:
            `QueryDefs <http://www.access2base.com/access2base.html#QueryDefs>`_
        """

    @overload
    def QueryDefs(self, index: str) -> _QueryDef:
        """
        Gets an instance of a query present in the current databse.

        Args:
            index (str): A QueryDef object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _QueryDef: QueryDef object.

        See Also:
            `QueryDefs <http://www.access2base.com/access2base.html#QueryDefs>`_
        """

    @overload
    def Recordsets(self) -> _Collection:
        """
        Gets instances of all recordsets that are currently open in relation with a given database object.

        Returns:
            _Collection: A Collection object.
        """

    @overload
    def Recordsets(self, index: int) -> _Recordset:
        """
        Gets a instance of a recordset this is currently open in relation with the given database object.

        Args:
            index (int): A Recordset object corresponding to the index-th item in the ~Recordsets() collection.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `Recordsets <http://www.access2base.com/access2base.html#Recordsets>`_
        """

    @overload
    def Recordsets(self, index: str) -> _Recordset:
        """
        Gets a instance of a recordset this is currently open in relation with the given database object.

        Args:
            index (str): A Recordset object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `Recordsets <http://www.access2base.com/access2base.html#Recordsets>`_
        """

    @overload
    def RunSQL(self, SQL: str) -> bool: ...

    @overload
    def RunSQL(self, SQL: str, option: int) -> bool:
        """
        Executes the SQL statement given as argument.

        The statement must execute an action.
        Typical statements are: INSERT INTO, DELETE, SELECT...INTO, UPDATE, CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX, or DROP INDEX.

        Args:
            SQL (str): Specifies the statement to execute
            option (int): If the argument is present its only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        Returns:
            bool: True on success.

        See Also:
            `RunSQL <http://www.access2base.com/access2base.html#RunSQL>`_
        """

    @overload
    def TableDefs(self) -> _Collection:
        """
        Gets instances of all tables present in the related database.

        Returns:
            _Collection: A Collection object

        See Also:
            `TableDefs <http://www.access2base.com/access2base.html#TableDefs>`_
        """

    @overload
    def TableDefs(self, index: int) -> _TableDef:
        """
        Gets a instance of a table present in the related databse.

        Args:
            index (int): A TableDef object corresponding to the index-th item in the TableDefs() collection.

        Returns:
            _TableDef: TableDef object.

        See Also:
            `TableDefs <http://www.access2base.com/access2base.html#TableDefs>`_
        """

    @overload
    def TableDefs(self, index: str) -> _TableDef:
        """
        Gets a instance of a table present in the related databse.

        Args:
            index (str): A TableDef object having the argument as name. The argument is NOT case-sensitive.

        Returns:
            _TableDef: TableDef object.

        See Also:
            `TableDefs <http://www.access2base.com/access2base.html#TableDefs>`_
        """
    # endregion Methods


class _Dialog(_BasicObject):
    ObjectType: Literal["DIALOG"]

    # region Properties
    @property
    def Caption(self) -> str:
        """
        Gets/Sets the text that appears in the title bar.
        """

    @property
    def Height(self) -> int:
        """
        Gets/Sets the height of the dialog.
        """

    @property
    def IsLoaded(self) -> bool:
        """
        Gets if dialog is active.
        """

    @property
    def OnFocusGained(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnFocusLost(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnKeyPressed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnKeyReleased(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseDragged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseEntered(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseExited(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseMoved(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMousePressed(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnMouseReleased(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def Page(self) -> int:
        """
        Gets/Sets the page on which the control is visible.
        """

    @property
    def Parent(self) -> Any:
        """
        Gets the parent object of the control.
        """

    @property
    def UnoDialog(self) -> XControl: ...

    @property
    def Width(self) -> int:
        """
        Gets/Sets the width of the dialog.
        """

    @property
    def Visible(self) -> bool:
        """
        Gets/Sets if a control is visible or hidden.
        """

    # endregion Properties

    # region Methods
    def EndExecute(self, returnvalue: int) -> None:
        """
        Interrupts programmatically the display of the specified dialog and transfers a value to be returned by the interrupted Execute method.

        Args:
            returnvalue (int): The value that will return the pending Execute method applied to the Dialog object

        Notes:
            * The EndExecute method must be preceeded with the Execute method applied on the same object.
            * The EndExecute method is usually triggered from a dialog or control event linked to the concerned dialog box.

        See Also:
            `EndExecute <http://www.access2base.com/access2base.html#EndExecute>`_
        """

    def Execute(self) -> int:
        """
        Displays the specified dialog.

        Returns:
            int: acConstants.dlgOK, acConstants.dlgCancel or
                The argument of the EndExecute method having requested the dialog closure

        See Also:
            `Execute <http://www.access2base.com/access2base.html#%5B%5BExecute%20(dialog)%5D%5D>`_
        """

    def Move(
            self, left: int = ..., top: int = ..., width: int = ..., height: int = ...
    ) -> bool:
        """
        Moves the specified object to the coordinates specified by the argument values.

        Args:
            left (int, optional): The screen position for the left edge of the form relative to the left edge of the screen.
            top (int, optional): The screen position for the top edge of the form relative to the top edge of the screen.
            width (int, optional): The desired width of the form.
            height (int, optional): The desired height of the form.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#Move>`_
        """

    def OptionGroup(self, groupname: str) -> Union[_OptionGroup, None]:
        """
        Gets an option group.

        Args:
            groupname (str): The name of the group = the name of its first element

        Returns:
            _OptionGroup | None: Option Group if found; Otherwise, None.
        """

    def Start(self) -> bool:
        """
        Initializes the specified dialog.

        Returns:
            bool: True on success.
        """

    def Terminate(self) -> bool:
        """
        Finalizes the specified dialog.

        Returns:
            bool: True on success.
        """
    # endregion Methods


class _Event(_BasicObject):
    ObjectType: Literal["EVENT"]

    # region Properties
    @property
    def ButtonLeft(self) -> bool:
        """
        Gets if the mouse button has been pressed.
        """

    @property
    def ButtonMiddle(self) -> bool:
        """
        Gets if the mouse button has been pressed.
        """

    @property
    def ButtonRight(self) -> bool:
        """
        Gets if the mouse button has been pressed.
        """

    @property
    def ClickCount(self) -> int:
        """
        Gets number of mouse clicks.
        """

    @property
    def ContextShortcut(self) -> str:
        """
        Gets the shortcut notation of the object (form, dialog or control) having triggered the event.
        """

    @property
    def EventName(self) -> str:
        """
        Gets event name.

        The following EventNames are commonly available:

        OnAlphaCharInput, OnClick, OnCloseApp, OnCopyTo, OnCopyToDone, OnCreate, OnError, OnFocus, OnInsertDone,
        OnInsertStart, OnLoad, OnLoadCancel, OnLoadDone, OnLoadError, OnLoadFinished, OnMailMerge,
        OnMailMergeFinished, OnModifyChanged, OnMouseOut, OnMouseOver, OnMove, OnNew, OnNewMail,
        OnNonAlphaCharInput, OnPageCountChange, OnPrepareUnload, OnPrepareViewClosing, OnPrint, OnResize,
        OnSave, OnSaveAs, OnSaveAsDone, OnSaveDone, OnSaveFinished, OnSelect, OnStartApp, OnSubComponentClosed,
        OnSubComponentOpened, OnTitleChanged, OnToggleFullscreen, OnUnfocus, OnUnload, OnViewClosed, OnViewCreated.
        """

    @property
    def EventType(self) -> str:
        """
        Gets Event Type

        See Also:
            `Events Handler <http://www.access2base.com/access2base.html#%5B%5BEvents%20Handler%5D%5D>`_
        """

    @property
    def FocusChangeTemporary(self) -> bool:
        """
        Gets focus change temporary.

        ``False`` if focus change due to a user action in same window.
        """

    @property
    def KeyAlt(self) -> bool:
        """
        Gets key combined with Alt, Ctrl or Shift keys.
        """

    @property
    def KeyCode(self) -> int:
        """
        Gets key combined with Alt, Ctrl or Shift keys.

        See Also:
            `Key Constant Group <https://tinyurl.com/y2gc43z7>`_
        """

    @property
    def KeyChar(self) -> str:
        """
        Gets the pressed key.
        """

    @property
    def KeyCtrl(self) -> bool:
        """
        Gets key combined with Alt, Ctrl or Shift keys.
        """

    @property
    def KeyFunction(self) -> int:
        """
        Gets the constants group ``com.sun.star.awt.KeyFunction``

        See Also:
            `KeyFunction Constant Group <https://tinyurl.com/y2yln9jj>`_
        """

    @property
    def KeyShift(self) -> bool:
        """
        Gets key combined with Alt, Ctrl or Shift keys.
        """

    @property
    def Recommendation(self) -> str:
        """
        Gets Recommendation.

        ``IGNORE`` if the event is recommended to be ignored.
        Valid only for the Before record action form event which is, for strange reasons,
        fired twice. The first time is recommended to be ignored.
        """

    @property
    def RowChangeAction(self) -> int:
        """
        Gets the constants group ``com.sun.star.sdb.RowChangeAction``

        See Also:
            `RowChangeAction Constant Group <https://tinyurl.com/yy8u3nzb>`_
        """

    @property
    def Source(self) -> Union[_Database, _Form, _SubForm, _Dialog, _Control]:
        """
        Gets the Database, Form, SubForm, Dialog or Control object having fired the event.
        """

    @property
    def SubComponentName(self) -> str:
        """
        Gets name of the component being opened or closed while executing a Loaded a sub component
        or Closed a sub component event. Such an event is set thru the Tools + Customize ... + Events
        menu command.
        """

    @property
    def SubComponentType(self) -> int:
        """
        Gets sub component type to be associated with the SubComponentName property.

        Returns one of next constants:

        - acConstants.acTable
        - acConstants.acQuery
        - acConstants.acForm
        - acConstants.acReport
        """

    @property
    def XPos(self) -> Union[int, None]:
        """
        Gets the mouse cursors X coordinate.

        Returns:
            int | None: X coordinate or None.
        """

    @property
    def YPos(self) -> Union[int, None]:
        """
        Gets the mouse cursors Y coordinate.

        Returns:
            int | None: Y coordinate or None.
        """
    # endregion Properties


class _Field(_BasicObject):
    ObjectType: Literal["FIELD"]

    # region Properties
    @property
    def Column(self) -> Any:
        """
        Gets column

        * com.sun.star.sdb.OTableColumnWrapper
        * org.openoffice.comp.dbaccess.OQueryColumn
        * com.sun.star.sdb.ODataColumn
        """

    @property
    def DataType(self) -> int:
        """
        Gets Data Type.

        - com.sun.star.sdbc.DataType.BIT
        - com.sun.star.sdbc.DataType.BOOLEAN
        - com.sun.star.sdbc.DataType.TINYINT
        - com.sun.star.sdbc.DataType.SMALLINT
        - com.sun.star.sdbc.DataType.INTEGER
        - com.sun.star.sdbc.DataType.BIGINT
        - com.sun.star.sdbc.DataType.FLOAT
        - com.sun.star.sdbc.DataType.REAL
        - com.sun.star.sdbc.DataType.DOUBLE
        - com.sun.star.sdbc.DataType.NUMERIC
        - com.sun.star.sdbc.DataType.DECIMAL
        - com.sun.star.sdbc.DataType.CHAR
        - com.sun.star.sdbc.DataType.VARCHAR
        - com.sun.star.sdbc.DataType.LONGVARCHAR
        - com.sun.star.sdbc.DataType.DATE
        - com.sun.star.sdbc.DataType.TIME
        - com.sun.star.sdbc.DataType.TIMESTAMP
        - com.sun.star.sdbc.DataType.BINARY
        - com.sun.star.sdbc.DataType.VARBINARY
        - com.sun.star.sdbc.DataType.LONGVARBINARY
        - com.sun.star.sdbc.DataType.CLOB
        - com.sun.star.sdbc.DataType.BLOB

        See Also:
            * `LibreOffice API DataType Constant Group <https://tinyurl.com/y2xhmuda>`_
            * `DataType <http://www.access2base.com/access2base.html#DataType>`_
        """

    @property
    def DataUpdatable(self) -> bool:
        """
        Gets if data is updatable
        """

    @property
    def DbType(self) -> int:
        """
        Gets Type

        - acConstants.dbBigInt
        - acConstants.dbBinary
        - acConstants.dbBoolean
        - acConstants.dbByte
        - acConstants.dbChar
        - acConstants.dbCurrency
        - acConstants.dbDate
        - acConstants.dbDecimal
        - acConstants.dbDouble
        - acConstants.dbFloat
        - acConstants.dbGUID
        - acConstants.dbInteger
        - acConstants.dbLong
        - acConstants.dbLongBinary
        - acConstants.dbMemo
        - acConstants.dbNumeric
        - acConstants.dbSingle
        - acConstants.dbText
        - acConstants.dbTime
        - acConstants.dbTimeStamp
        - acConstants.dbVarBinary
        - acConstants.dbUndefined

        See Also:
            `DataType <http://www.access2base.com/access2base.html#DataType>`_
        """

    @property
    def DefaultValue(self) -> str:
        """
        Gets/Sets default value of field.
        """

    @property
    def Description(self) -> str:
        """
        Gets/Sets summary description of the field
        """

    @property
    def FieldSize(self) -> int:
        """
        Gets the number of bytes used in the database (rather than in memory) of a Memo or Long Binary Field
        object in the Fields collection of a Recordset object.
        """

    @property
    def Size(self) -> int:
        """
        Gets the maximum size of the field
        """

    @property
    def Source(self) -> Union[_Database, _Form, _SubForm, _Dialog, _Control]:
        """
        Gets the Database, Form, SubForm, Dialog or Control object having fired the event.
        """

    @property
    def SourceField(self) -> str:
        """
        Gets a value that indicates the name of the field that is the original source of the data for a Field object.
        """

    @property
    def SourceTable(self) -> str:
        """
        Gets a value that indicates the name of the table that is the original source of the data for a Field object.
        """

    @property
    def TypeName(self) -> str:
        """
        Gets the AOO/LibO type of the data as a string.

        See Also:
            * `DataType <http://www.access2base.com/access2base.html#DataType>`_
        """

    @property
    def Value(self) -> Any:
        """
        Gets the value stored or to be stored in the field.
        """

    # endregion Properties

    # region Methods
    def AppendChunk(self, value: Any) -> bool:
        """
        Store a chunk of string or binary characters into the current field, presumably a large object (CLOB or BLOB)

        Args:
            value (Any): Data to append

        Returns:
            bool: True if success.
        """

    def GetChunk(self, offset: int, numbytes: int) -> Any:
        """
        Get a chunk of string or binary characters from the current field, presumably a large object (CLOB or BLOB)
        """

    def ReadAllBytes(self, file: str) -> bool:
        """
        Imports the content of a file specified by its full name into a binary Field belonging to a Recordset.

        Args:
            file (str): The full name, including the path, of the file you want to import the data from.

        Returns:
            bool: True on success.

        See Also:
            `ReadAllBytes <http://www.access2base.com/access2base.html#ReadAllBytes>`_
        """

    def ReadAllText(self, file: str) -> bool:
        """
        Imports the content of a file specified by its full name into a memo Field belonging to a Recordset.

        Args:
            file (str): The full name, including the path, of the file you want to import the data from.

        Returns:
            bool: True on success.

        See Also:
            `ReadAllText <http://www.access2base.com/access2base.html#ReadAllText>`_
        """

    def WriteAllBytes(self, file: str) -> bool:
        """
        Writes the content of a binary Field belonging to a Recordset to a file specified by its full name.

        Args:
            file (str): The full name, including the path, of the file you want to output the data to.

        Returns:
            bool: True on success.

        See Also:
            `WriteAllBytes <http://www.access2base.com/access2base.html#WriteAllBytes>`_
        """

    def WriteAllText(self, file: str) -> bool:
        """
        Writes the content of a memo Field belonging to a Recordset to a file specified by its full name.

        Args:
            file (str): The full name, including the path, of the file you want to output the data to.

        Returns:
            bool: True on success.

        See Also:
            `WriteAllText <http://www.access2base.com/access2base.html#WriteAllText>`_
        """
    # endregion Methods


class _Form(_BasicObject):
    ObjectType: Literal["FORM"]

    # region Properties
    @property
    def AllowAdditions(self) -> bool:
        """
        Get/Sets whether a user can add a record when using the form.
        """

    @property
    def AllowDeletions(self) -> bool:
        """
        Get/Sets whether a user can delete a record when using the form.
        """

    @property
    def AllowEdits(self) -> bool:
        """
        Get/Sets whether a user can modify a record when using the form.
        """

    @property
    def Bookmark(self) -> Any:
        """
        Get/Sets uniquely the current record of the form's underlying table, query or SQL statement.

        See Also:
            `Bookmark <http://www.access2base.com/access2base.html#Bookmark>`_
        """

    @property
    def Caption(self) -> str:
        """
        Get/Sets the text that appears in the title bar.
        """

    @property
    def Component(self) -> UnoTextDocument:
        """
        Gets component.

        Returns:
            TextDocument: Text Document
        """

    @property
    def ContainerWindow(self) -> XWindow:
        """
        Gets container window.
        """

    @property
    def CurrentRecord(self) -> int:
        """
        Get/Sets the current record in the recordset being viewed on a form.

        See Also:
            `CurrentRecord <http://www.access2base.com/access2base.html#CurrentRecord>`_
        """

    @property
    def DatabaseForm(self) -> Union[DataForm, ResultSet]:
        """
        Gets Database Form
        """

    @property
    def Filter(self) -> str:
        """
        Get/Sets Specifies a subset of records to be displayed.

        See Also:
            `Filter <http://www.access2base.com/access2base.html#Filter>`_
        """

    @property
    def FilterOn(self) -> bool:
        """
        Gets/Sets if the Filter has to be applied.

        See Also:
            `FilterOn <http://www.access2base.com/access2base.html#FilterOn>`_
        """

    @property
    def Height(self) -> int:
        """
        Gets/Sets the height of the form.
        """

    @property
    def IsLoaded(self) -> bool:
        """
        Gets if form is open.
        """

    @property
    def OnApproveCursorMove(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveParameter(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveReset(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveRowChange(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnApproveSubmit(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnConfirmDelete(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnCursorMoved(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnErrorOccurred(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnLoaded(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnReloaded(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnReloading(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnResetted(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnRowChanged(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnUnloaded(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OnUnloading(self) -> str:
        """
        Gets/Sets which function is triggered when a control event occurs.
        """

    @property
    def OpenArgs(self) -> Any:
        """
        Gets the expression that was passed as argument of an OpenForm action.

        See Also:
            `OpenArgs <http://www.access2base.com/access2base.html#OpenArgs>`_
        """

    @property
    def OrderBy(self) -> str:
        """
        Gets/Sets in which order the records should be displayed.

        See Also:
            `OrderBy <http://www.access2base.com/access2base.html#OrderBy>`_
        """

    @property
    def OrderByOn(self) -> bool:
        """
        Gets/Sets if the OrderBy has to be applied.

        See Also:
            `OrderByOn <http://www.access2base.com/access2base.html#OrderByOn>`_
        """

    @property
    def Parent(self) -> Any:
        """
        Gets the parent object of the control.
        """

    @property
    def Recordset(self) -> _Recordset:
        """
        Gets record set
        """

    @property
    def RecordSource(self) -> str:
        """
        Gets/Sets the source of the data.

        See Also:
            `RecordSource <http://www.access2base.com/access2base.html#RecordSource>`_
        """

    @property
    def Visible(self) -> bool:
        """
        Gets/Sets if the form is visible or hidden.
        """

    @property
    def Width(self) -> int:
        """
        Gets/Sets the width of the form.
        """

    # endregion Properties

    # region Methods
    def Close(self) -> bool:
        """
        Close the form.

        Returns:
            bool: Always returns ``True``.
        """

    @overload
    def Controls(self) -> _Collection: ...

    @overload
    def Controls(self, index: Union[str, int]) -> _Control: ...

    def Move(
            self, left: int = ..., top: int = ..., width: int = ..., height: int = ...
    ) -> bool:
        """
        Moves the specified object to the coordinates specified by the argument values.

        Args:
            left (int, optional): The screen position for the left edge of the form relative to the left edge of the screen.
            top (int, optional): The screen position for the top edge of the form relative to the top edge of the screen.
            width (int, optional): The desired width of the form.
            height (int, optional): The desired height of the form.

        Returns:
            bool: ``True ``on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#Move>`_
        """

    def OptionGroup(self, groupname: str) -> Union[_OptionGroup, None]:
        """
        Gets an option group.

        Args:
            groupname (str): The name of the group = the name of its first element

        Returns:
            _OptionGroup | None: Option Group if found; Otherwise, None.
        """

    def Refresh(self) -> bool:
        """
        Refresh data with its most recent value in the database.

        Returns:
            bool: True on success.
        """

    def Requery(self) -> bool:
        """
        Refresh the data displayed in the Form.

        Returns:
            bool: True on success.
        """

    def SetFocus(self) -> bool:
        """
        Set focus on Form.

        Returns:
            bool: True on success.
        """
    # endregion Methods


class _Module(_BasicObject):
    """
    A Module object represents a module containing a Basic script. It might represent either a
    standard module or a class module.

    See Also:
        `Module <http://www.access2base.com/access2base.html#Module>`_
    """
    ObjectType: Literal["MODULE"]

    def __init__(
            self, reference: int = ..., objtype: Any = ..., name: str = ...
    ) -> None: ...

    # region Properties
    @property
    def CountOfDeclarationLines(self) -> int:
        """
        Gets the number of lines of code in the Declarations section in a standard or class module.
        """

    @property
    def CountOfLines(self) -> int:
        """
        Gets the number of lines of code in the module.
        """

    @property
    def Type(self) -> int:
        """
        Gets the type of a query, a commandbarcontrol or a Basic module.

        Returns a const value from acConstants.

        See Also:
            `Type <http://www.access2base.com/access2base.html#Type>`_
        """

    # endregion Properties

    # region Methods
    def Find(
            self,
            target: str,
            startline: int,
            startcolumn: int,
            endline: int,
            endcolumn: int,
            wholeword: bool = ...,
            matchcase: bool = ...,
            patternsearch: bool = ...,
    ) -> bool:
        """
        Finds a specified text in a standard or class module.

        Args:
            target (str): The text that you want to find.

            startline (int): The line on which to begin searching. If a match is found, the value of the startline
                argument is set to the line on which the beginning character of the matching text is found.

            startcolumn (int): The column on which to begin searching. If a match is found, the value of the startcolumn
                argument is set to the column on which the beginning character of the matching text is found.

            endline (int): The line on which to stop searching. If a match is found, the value of the endline
                argument is set to the line on which the ending character of the matching text is found.

            endcolumn (int): The column on which to stop searching. If a match is found, the value of the endcolumn
                argument is set to the column on which the ending character of the matching text is found.

            wholeword (bool, optional): True results in a search for whole words only. The default is False.

            matchcase (bool, optional): True results in a search for words with case matching the target argument.
                The default is False.

            patternsearch (bool, optional): True results in a search in which the target argument may contain
                wildcard characters such as an asterisk (*) or a question mark (?). The default is False.

        Returns:
            bool: True If the string is found; Otherwise, False.

        See Also:
            `Find <http://www.access2base.com/access2base.html#Find>`_
        """

    def Lines(self, line: int, numlines: int) -> str:
        """
        Gets a string containing the contents of a specified line or lines in a standard or a class

        Args:
            line (int): The number of the first line to return.
            numlines (int): The number of lines to return.

        Returns:
            str: line(s)

        Notes:
            The requested lines are returned as one single string. The individual lines are separated by a line
            feed (Chr(10)) character. Lines in a module are numbered beginning with 1. For example,
            if you read the Lines property with a value of 1 for the line argument and 1 for the numlines argument,
            the Lines property returns a string containing the text of the first line in the module.

        See Also:
            `Lines <http://www.access2base.com/access2base.html#Lines>`_
        """

    def ProcBodyLine(self, procname: str, prockind: int) -> int:
        """
        Gets the number of the line at which the body of a specified procedure
        begins in a standard or a class module.

        Args:
            procname (str): The name of a procedure in the module.
            prockind (int): The type of procedure.

        Returns:
            int: number of lines

        Note:
            **Arg** ``prockind`` can be one of the following constants:

            - acConstants.vbext_pk_Get
            - acConstants.vbext_pk_Let
            - acConstants.vbext_pk_Proc
            - acConstants.vbext_pk_Set

        See Also:
            `ProcBodyLine <http://www.access2base.com/access2base.html#ProcBodyLine>`_
        """

    def ProcCountLines(self, procname: str, prockind: int) -> int:
        """
        Gets the number of lines in a specified procedure in a standard or a class module.

        Args:
            procname (str): The name of a procedure in the module.
            prockind (int): The type of procedure.

        Returns:
            int: number of lines

        Note:
            **Arg** ``prockind`` can be one of the following constants:

            - acConstants.vbext_pk_Get
            - acConstants.vbext_pk_Let
            - acConstants.vbext_pk_Proc
            - acConstants.vbext_pk_Set

        See Also:
            `ProcCountLines <http://www.access2base.com/access2base.html#ProcCountLines>`_
        """

    def ProcOfLine(self, line: int, prockind: int) -> str:
        """
        Gets the name of the procedure that contains a specified line in a standard or a class module.

        Args:
            line (int): The number of a line in the module.
            prockind (int): The type of procedure.

        Returns:
            str: number of lines

        Note:
            **Arg** ``prockind`` can be one of the following constants:

            - acConstants.vbext_pk_Get
            - acConstants.vbext_pk_Let
            - acConstants.vbext_pk_Proc
            - acConstants.vbext_pk_Set

        See Also:
            `ProcOfLine <http://www.access2base.com/access2base.html#ProcOfLine>`_
        """

    def ProcStartLine(self, procname: str, prockind: int) -> int:
        """
        Gets a value identifying the line at which a specified procedure begins in a standard or a class module.

        Args:
            procname (str): The name of a procedure in the module.
            prockind (int): The type of procedure.

        Returns:
            int: number of line

        Note:
            **Arg** ``prockind`` can be one of the following constants:

            - acConstants.vbext_pk_Get
            - acConstants.vbext_pk_Let
            - acConstants.vbext_pk_Proc
            - acConstants.vbext_pk_Set

        See Also:
            `ProcStartLine <http://www.access2base.com/access2base.html#ProcStartLine>`_
        """
    # endregion Methods


class _OptionGroup(_BasicObject):
    ObjectType: Literal["OPTIONGROUP"]

    # region Properties
    @property
    def Count(self) -> int:
        """
        Gets the number of radio buttons belonging to the group.
        """

    @property
    def Value(self) -> int:
        """
        Gets/Sets the index of the radio button being currently selected.
        """

    # endregion Properties

    # region Methods
    @overload
    def Controls(self) -> _Collection: ...

    @overload
    def Controls(self, index: Union[str, int]) -> _Control: ...
    # endregion Methods


class _Property(_BasicObject):
    ObjectType: Literal["PROPERTY"]

    @property
    def Value(self) -> Any:
        """
        Gets/Sets the value of the considered property (might be an array).
        """


class _QueryDef(_BasicObject):
    ObjectType: Literal["QUERYDEF"]

    # region Properties
    @property
    def Query(self) -> Any: ...

    @property
    def SQL(self) -> str:
        """
        Gets/Sets the SQL statement related to the query
        """

    @property
    def Type(self) -> int:
        """
        Gets Classification of the query.

        ``Type`` is a value from ``acConstants``.

        See Also:
            `Type <http://www.access2base.com/access2base.html#Type>`_
        """

    # endregion Properties

    # region Methods
    @overload
    def Execute(self) -> None: ...

    @overload
    def Execute(self, options: int) -> None:
        """
        Executes the SQL statement contained in a query.
        The statement must execute an action.

        Examples of such statements are: INSERT INTO, DELETE, SELECT...INTO, UPDATE, CREATE TABLE, ALTER TABLE, DROP TABLE, CREATE INDEX, or DROP INDEX.

        Args:
            options (int): only allowed value is acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

        See Also:
            `Execute <http://www.access2base.com/access2base.html#%5B%5BExecute%20(query)%5D%5D>`_
        """

    @overload
    def Fields(self) -> _Collection:
        """
        Gets the collection of the fields belonging to the query.

        Returns:
            _Collection: Collection object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: int) -> _Field:
        """
        Gets a field from the fields belonging to the query.

        Args:
            index (int): A Field object corresponding to the index-th item in the
                Field()

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: str) -> _Field:
        """
        Gets a field from the fields belonging to the query.

        Args:
            index (str): A Field object having the argument as name.
                The argument is NOT case-sensitive.

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    def OpenRecordset(
            self, type: int = ..., option: int = ..., lockedit: int = ...
    ) -> _Recordset:
        """
        Gets a new Recordset object and appends it to the Recordsets collection of the concerned database object.

        Args:
            type (int, optional): If the argument is present its only allowed value is acConstants.dbOpenForwardOnly.
                Forces one-directional browsing of the records.

            option (int, optional): f the argument is present its only allowed value = acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

            lockedit (int, optional): If the argument is present its only allowed value is acConstants.dbReadOnly.
                Forces dirty read and prevents from database updates.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `OpenRecordset <http://www.access2base.com/access2base.html#OpenRecordset>`_
        """
    # endregion Methods


class _Recordset(_BasicObject):
    ObjectType: Literal["RECORDSET"]

    # region Properties
    @property
    def AbsolutePosition(self) -> int:
        """
        Gets/Sets the relative record number of a Recordset object's current record.
        """

    @property
    def BOF(self) -> bool:
        """
        Gets a value that indicates whether the current record position is before the first record in a Recordset object.
        """

    @property
    def Bookmark(self) -> Any:
        """
        Get/Sets uniquely the current record of the form's underlying Recordset object.

        See Also:
            `Bookmark <http://www.access2base.com/access2base.html#Bookmark>`_
        """

    @property
    def Bookmarkable(self) -> bool:
        """
        Gets a value that indicates whether a Recordset object supports bookmarks,
        which you can set by using the Bookmark property.
        """

    @property
    def EditMode(self) -> int:
        """
        Gets a value that indicates the state of editing for the current record.

        - acConstants.dbEditNone - No editing operation is in progress.
        - acConstants.dbEditInProgress - The Edit method has been invoked, and the current record is in the edit buffer.
        - acConstants.dbEditAdd - The AddNew method has been invoked, and the current record in the edit buffer is a new record that hasn't been saved in the database.

        See Also:
            `EditMode <http://www.access2base.com/access2base.html#EditMode>`_
        """

    @property
    def EOF(self) -> bool:
        """
        Gets a value that indicates whether the current record position is after the last record in a Recordset object.
        """

    @property
    def Filter(self) -> str:
        """
        Get/Sets a value that determines the records included in a subsequently opened
        Recordset object (via OpenRecordset)

        See Also:
            `Filter <http://www.access2base.com/access2base.html#Filter>`_
        """

    @property
    def RecordCount(self) -> int:
        """
        Gets the number of records of the recordset.
        """

    @property
    def RowSet(self) -> UnoRowSet:
        """Gets row set."""

    # endregion Properties

    # region Methods
    def AddNew(self) -> bool:
        """
        Initiate the creation of a new record.

        Returns:
            bool: True on success.

        See Also:
            `AddNew <http://www.access2base.com/access2base.html#AddNew>`_
        """

    def CancelUpdate(self) -> bool:
        """
        Cancels any pending updates for a Recordset object.

        Returns:
            bool: True on success.

        See Also:
            `CancelUpdate <http://www.access2base.com/access2base.html#CancelUpdate>`_
        """

    def Clone(self) -> _Recordset:
        """
        Creates a duplicate Recordset object that refers to the original Recordset object..

        Returns:
            _Recordset: Recordset object

        See Also:
            `Clone <http://www.access2base.com/access2base.html#Clone>`_
        """

    def Close(self) -> None:
        """
        Closes the recordset

        See Also:
            `Close <http://www.access2base.com/access2base.html#%5B%5BClose%20(method)%5D%5D>`_
        """

    def Delete(self) -> bool:
        """
        Deletes the current record in an updatable Recordset object.

        Returns:
            bool: True on success.

        See Also:
            `Delete <http://www.access2base.com/access2base.html#Delete>`_
        """

    def Edit(self) -> bool:
        """
        Copies the current record from an updatable Recordset object to the edit buffer for subsequent editing.

        Returns:
            bool: True on success.

        See Also:
            `Edit <http://www.access2base.com/access2base.html#Edit>`_
        """

    @overload
    def Fields(self) -> _Collection:
        """
        Gets the collection of the fields belonging to the Recordset.

        Returns:
            _Collection: Collection object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: int) -> _Field:
        """
        Gets a field from the fields belonging to the Recordset.

        Args:
            index (int): A Field object corresponding to the index-th item in the
                Field()

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: str) -> _Field:
        """
        Gets a field from the fields belonging to the Recordset.

        Args:
            index (str): A Field object having the argument as name.
                The argument is NOT case-sensitive.

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    def GetRows(self, numrows: int) -> list[list]:
        """
        Retrieves multiple rows from a Recordset object.

        Args:
            numrows (int): the maximum number of rows to retrieve

        Returns:
            Any: a two-dimensional array. The first subscript identifies the field and the second identifies the row number.

        See Also:
            `GetRows <http://www.access2base.com/access2base.html#GetRows>`_
        """

    @overload
    def Move(self, rows: int) -> bool: ...

    @overload
    def Move(self, rows: int, startbookmark: Any) -> bool:
        """
        Moves to a record specified by its position

        Args:
            rows (int): Specifies the number of rows the position will move.
                If rows is greater than 0, the position is moved forward (toward the end of the file).
                If rows is less than 0, the position is moved backward (toward the beginning of the file).
            startbookmark (Any): Value identifying a bookmark. If you specify startbookmark, the move begins relative to this bookmark.
                Otherwise, move begins from the current record.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#%5B%5BMove%20(recordset)%5D%5D>`_
        """

    def MoveFirst(self) -> bool:
        """
        Moves to first record.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#%5B%5BMove%20(recordset)%5D%5D>`_
        """

    def MoveLast(self) -> bool:
        """
        Moves to last record.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#%5B%5BMove%20(recordset)%5D%5D>`_
        """

    def MoveNext(self) -> bool:
        """
        Moves to Next record.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#%5B%5BMove%20(recordset)%5D%5D>`_
        """

    def MovePrevious(self) -> bool:
        """
        Moves to previous record.

        Returns:
            bool: True on success.

        See Also:
            `Move <http://www.access2base.com/access2base.html#%5B%5BMove%20(recordset)%5D%5D>`_
        """

    def OpenRecordset(
            self, type: int = ..., option: int = ..., lockedit: int = ...
    ) -> _Recordset:
        """
        Gets a new Recordset object and appends it to the Recordsets collection of the concerned database object.

        Args:
            type (int, optional): If the argument is present its only allowed value is acConstants.dbOpenForwardOnly.
                Forces one-directional browsing of the records.

            option (int, optional): f the argument is present its only allowed value = acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

            lockedit (int, optional): If the argument is present its only allowed value is acConstants.dbReadOnly.
                Forces dirty read and prevents from database updates.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `OpenRecordset <http://www.access2base.com/access2base.html#OpenRecordset>`_
        """

    def Update(self) -> bool:
        """
        Saves the contents of the edit buffer to an updatable Recordset object.

        Returns:
            bool: True on success.

        See Also:
            `Update <http://www.access2base.com/access2base.html#Update>`_
        """
    # endregion Methods


class _SubForm(_Form):
    ObjectType: Literal["SUBFORM"]

    # region Properties
    @property
    def AllowAdditions(self) -> bool:
        """
        Gets/Sets whether a user can add a record when using a form or a subform.

        See Also:
            `AllowAdditions <http://www.access2base.com/access2base.html#AllowAdditions>`_
        """

    @property
    def AllowDeletions(self) -> bool:
        """
        Gets/Sets whether a user can delete a record when using a form or a subform.

        See Also:
            `AllowAdditions <http://www.access2base.com/access2base.html#AllowDeletions>`_
        """

    @property
    def AllowEdits(self) -> bool:
        """
        Gets/Sets whether a user can edit saved records when using a form or a subform.

        See Also:
            `AllowAdditions <http://www.access2base.com/access2base.html#AllowEdits>`_
        """

    @property
    def CurrentRecord(self) -> int:
        """
        Get/Sets the current record in the recordset being viewed on a subform.

        See Also:
            `CurrentRecord <http://www.access2base.com/access2base.html#CurrentRecord>`_
        """

    @property
    def LinkChildFields(self) -> Tuple[str, ...]:
        """
        Gets how records in the subform (child) are linked to records in its parent (master) form.

        See Also:
            `LinkChildFields <http://www.access2base.com/access2base.html#LinkChildFields>`_
        """

    @property
    def LinkMasterFields(self) -> Tuple[str, ...]:
        """
        Gets how records in the subform (child) are linked to records in its parent (master) form.

        See Also:
            `LinkMasterFields <http://www.access2base.com/access2base.html#LinkMasterFields>`_
        """
    # endregion Properties


class _TableDef(_BasicObject):
    ObjectType: Literal["TABLEDEF"]

    @property
    def Table(self) -> UnoTable:
        """
        Gets Table
        """

    def CreateField(
            self, name: str, type: int, size: Number = ..., attributes: int = ...
    ) -> _Field:
        """
        Appends a new Field object to a table.

        This method offers the capacity to create from the Basic code a new table field independently
        from the underlying RDBMS. Thus without using SQL. However only a limited set of options are
        available for field descriptions.

        Args:
            name (str): The name of the new field
            type (int): The database type ("DbType") of the new field. See Type Property section of acConstants.
            size (Number, optional): The length of the field. It is ignored when not relevant.
                If size has a non-integer value, the first decimal digit at the right of the decimal
                point determines the number of decimal digits.
            attributes (int, optional): Indicates if present that the field is a primary key and is incremented
                by the RDBMS at each new record insertion.

        Returns:
            _Field: Field object

        See Also:
            `CreateField <http://www.access2base.com/access2base.html#CreateField>`_
        """

    @overload
    def Fields(self) -> _Collection:
        """
        Gets the collection of the fields belonging to the query.

        Returns:
            _Collection: Collection object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: int) -> _Field:
        """
        Gets a field from the fields belonging to the query.

        Args:
            index (int): A Field object corresponding to the index-th item in the
                Field()

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    @overload
    def Fields(self, index: str) -> _Field:
        """
        Gets a field from the fields belonging to the query.

        Args:
            index (str): A Field object having the argument as name.
                The argument is NOT case-sensitive.

        Returns:
            _Field: a Field object.

        See Also:
            `Fields <http://www.access2base.com/access2base.html#Fields>`_
        """

    def OpenRecordset(
            self, type: int = ..., option: int = ..., lockedit: int = ...
    ) -> _Recordset:
        """
        Gets a new Recordset object and appends it to the Recordsets collection of the concerned database object.

        Args:
            type (int, optional): If the argument is present its only allowed value is acConstants.dbOpenForwardOnly.
                Forces one-directional browsing of the records.

            option (int, optional): If the argument is present its only allowed value = acConstants.dbSQLPassThrough.
                Forces escape substitution before sending the SQL statement to the database.

            lockedit (int, optional): If the argument is present its only allowed value is acConstants.dbReadOnly.
                Forces dirty read and prevents from database updates.

        Returns:
            _Recordset: Recordset object.

        See Also:
            `OpenRecordset <http://www.access2base.com/access2base.html#OpenRecordset>`_
        """


class _TempVar(_BasicObject):
    ObjectType: Literal["TEMPVAR"]

    @property
    def Value(self) -> Any:
        """
        Gets/Sets the value of the considered variable (might be any value that can be
        stored, including arrays or objects).
        """


###
# Set of directly callable error handling methods
###


def DebugPrint(*args: Any) -> None: ...


def TraceConsole() -> None: ...


def TraceError(
        tracelevel: str, errorcode: int, errorprocedure: str, errorline: int
) -> None: ...


def TraceLevel(newtracelevel: str = ...) -> None: ...


@overload
def TraceLog(tracelevel: str, text: str) -> None: ...


@overload
def TraceLog(tracelevel: str, text: str, messagebox: bool) -> None: ...
