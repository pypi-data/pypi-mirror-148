# -*- coding: utf-8 -*-
"""\
* *[pyIcmLib]* :: Operations Abstract Base Classes.
"""

import typing

icmInfo: typing.Dict[str, typing.Any] = { 'moduleDescription': ["""
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Description:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Xref]          :: *[Related/Xrefs:]*  <<Xref-Here->>  -- External Documents  [[elisp:(org-cycle)][| ]]
**  [[elisp:(org-cycle)][| ]]   Model and Terminology                                      :Overview:
** In Native-BISOS the primary entry to all that is executed is an Operation.
** All operations are derived from the class AbstractOperation.
** There are 4 abstractions under the AbstractOperation.
** 1) Operations Support Facilities, logging, tracing, audit-trail, etc.
** 2) AbstractWithinOperationWrappers: Wrappers that are aware of the context of operations
** 3) AbstractRemoteOperations: For when an Operation is delegated to remote performance
** 4) AbstractCommands: For enabling consistent invitation of Operations from command line.
**      [End-Of-Description]
"""], }

icmInfo['moduleUsage'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Usage:* | ]]
** +
** These classes are to be sub-classed. There is no explicit direct usage.
**      [End-Of-Usage]
"""

icmInfo['moduleStatus'] = """
*       [[elisp:(org-show-subtree)][|=]]  [[elisp:(org-cycle)][| *Status:* | ]]
**  [[elisp:(org-cycle)][| ]]  [Info]          :: *[Current-Info:]* Status/Maintenance -- General TODO List [[elisp:(org-cycle)][| ]]
** TODO Revisit implementation of all classes based on existing ICM.
SCHEDULED: <2021-12-18 Sat>
** TODO Transition to op.AbstractCommand from icm.Cmnd
** TODO Fully shape up this module to reflect best templates.
**      [End-Of-Status]
"""

"""
*  [[elisp:(org-cycle)][| *ICM-INFO:* |]] :: Author, Copyleft and Version Information
"""
####+BEGIN: bx:icm:py:name :style "fileName"
icmInfo['moduleName'] = "pattern"
####+END:

####+BEGIN: bx:icm:py:version-timestamp :style "date"
icmInfo['version'] = "202110191256"
####+END:

####+BEGIN: bx:icm:py:status :status "Production"
icmInfo['status']  = "Production"
####+END:

icmInfo['credits'] = ""

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/update/sw/icm/py/icmInfo-mbNedaGplByStar.py"
icmInfo['authors'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['copyright'] = "Copyright 2017, [[http://www.neda.com][Neda Communications, Inc.]]"
icmInfo['licenses'] = "[[https://www.gnu.org/licenses/agpl-3.0.en.html][Affero GPL]]", "Libre-Halaal Services License", "Neda Commercial License"
icmInfo['maintainers'] = "[[http://mohsen.1.banan.byname.net][Mohsen Banan]]"
icmInfo['contacts'] = "[[http://mohsen.1.banan.byname.net/contact]]"
icmInfo['partOf'] = "[[http://www.by-star.net][Libre-Halaal ByStar Digital Ecosystem]]"
####+END:

icmInfo['panel'] = "{}-Panel.org".format(icmInfo['moduleName'])
icmInfo['groupingType'] = "IcmGroupingType-pkged"
icmInfo['cmndParts'] = "IcmCmndParts[common] IcmCmndParts[param]"


####+BEGIN: bx:icm:python:top-of-file :partof "bystar" :copyleft "halaal+minimal"
"""
*  This file:/bisos/git/auth/bxRepos/bisos-pip/basics/py3/bisos/basics/pattern.py :: [[elisp:(org-cycle)][| ]]
 is part of The Libre-Halaal ByStar Digital Ecosystem. http://www.by-star.net
 *CopyLeft*  This Software is a Libre-Halaal Poly-Existential. See http://www.freeprotocols.org
 A Python Interactively Command Module (PyICM).
 Best Developed With COMEEGA-Emacs And Best Used With Blee-ICM-Players.
 *WARNING*: All edits wityhin Dynamic Blocks may be lost.
"""
####+END:

####+BEGIN: bx:icm:python:topControls :partof "bystar" :copyleft "halaal+minimal"
"""
*  [[elisp:(org-cycle)][|/Controls/| ]] :: [[elisp:(org-show-subtree)][|=]]  [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(delete-other-windows)][(1)]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]
"""
####+END:
####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/pyWorkBench.org"
"""
*  /Python Workbench/ ::  [[elisp:(org-cycle)][| ]]  [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
"""
####+END:

####+BEGIN: bx:icm:python:icmItem :itemType "=Imports=" :itemTitle "*IMPORTS*"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  =Imports=  :: *IMPORTS*  [[elisp:(org-cycle)][| ]]
"""
####+END:

from unisos import ucf
from unisos import icm

from enum import Enum

####+BEGIN: bx:dblock:python:class :className "OpError" :superClass "Enum" :comment "" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /OpError/ Enum  [[elisp:(org-cycle)][| ]]
"""
class OpError(Enum):
    ####+END:
    Success = 0
    Failure = 1
    ShellBuiltinMisuse = 2
    ExtractionSuccess = 11
    PermissionProblem = 126
    CommandNotFound = 127
    ExitError = 128
    Signal1 = 128+1
    ControlC = 130
    Signal9 = 128+9
    UsageError = 201
    CmndLineUsageError = 202
    ExitStatusOutOfRange = 255



opErrorDesc = {}

opErrorDesc[OpError.Success] = "Successful Operation -- No Errors"
opErrorDesc[OpError.Failure] = "Catchall for general errors"
opErrorDesc[OpError.ShellBuiltinMisuse]= "Bash Problem"
opErrorDesc[OpError.ExtractionSuccess] = "NOTYET"
opErrorDesc[OpError.PermissionProblem] = "Command invoked cannot execute"


####+BEGIN: bx:dblock:python:func :funcName "notAsFailure" :funcType "succFail" :retType "bool" :deco "" :argsList "obj"
"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]] [[elisp:(show-children)][|V]] [[elisp:(org-tree-to-indirect-buffer)][|>]] [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func-succFail  :: /notAsFailure/ retType=bool argsList=(obj)  [[elisp:(org-cycle)][| ]]
"""
def notAsFailure(
    obj,
):
####+END:
    if not obj:
        return  OpError.Failure
    else:
        return  OpError.Success


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  opErrorDescGet -- return opErrorDesc[opError]   [[elisp:(org-cycle)][| ]]
"""
def opErrorDescGet(opError):
    """ OpError is defined as Constants. A basic textual description is provided with opErrorDescGet().

Usage:  opOutcome.error = None  -- opOutcome.error = OpError.UsageError
OpError, eventually maps to Unix sys.exit(error). Therefore, the range is 0-255.
64-to-78 Should be made consistent with /usr/include/sysexits.h.
There are also qmail errors starting at 100.
"""
    # NOTYET, catch exceptions
    return opErrorDesc[opError]



"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Class-Basic        ::  Outcome -- .log() .isProblematic()   [[elisp:(org-cycle)][| ]]
"""
class Outcome(object):
    """ Operation Outcome. Consisting Of Error and/or Result -- Operation Can Be Local Or Remote

** TODO Add exception and exceptionInfo For situations where try: is handled
** TODO Add opType as one of PyCallable -- SubProc, RemoteOp
** TODO Add a printer (repr) for Outcome

Outcome is a combination of OpError(SuccessOrError) and OpResults.

Typical Usage is like this:

On Definition of f():
thisOutcome = Outcome()
thisOutcome.results = itemOrList
)
return(thisOutcome.set(
    opError=None,
    ))

Then on invocation:
thisOutcome = Outcome()
opOutcome = f()
if opOutcome.error: return(thisOutcome.set(opError=opOutcome.error))
opResults = opOutcome.results
"""
    def __init__(self,
                 invokerName=None,
                 opError=None,
                 opErrInfo=None,
                 opResults=None,
                 opStdout=None,
                 opStderr=None,
                 opStdcmnd=None,
    ):
        '''Constructor'''
        self.invokerName = invokerName
        self.error = opError
        self.errInfo  = opErrInfo
        self.results = opResults
        self.stdout = opStdout
        self.stderr = opStderr
        self.stdcmnd = opStdcmnd

    def set(self,
            invokerName=None,
            opError=None,
            opErrInfo=None,
            opResults=None,
            opStdout=None,
            opStderr=None,
            opStdcmnd=None,
    ):
        if invokerName != None:
            self.name = invokerName
        if opError != None:
            self.error = opError
        if opErrInfo != None:
            self.errInfo = opErrInfo
        if opResults != None:
            self.results = opResults
        if opStdout != None:
            self.stdout = opStdout
        if opStderr != None:
            self.stderr = opStderr
        if opStdcmnd != None:
            self.stdcmnd = opStdcmnd

        return self

    def isProblematic(self):
        if self.error:
            icm.IcmGlobalContext().__class__.lastOutcome = self
            return True
        else:
            return False


    def log(self):
        G = icm.IcmGlobalContext()
        icm.LOG_here(G.icmMyFullName() + ':' + str(self.invokerName) + ':' + ucf.stackFrameInfoGet(2))
        if self.stdcmnd: icm.LOG_here("Stdcmnd: " +  self.stdcmnd)
        if self.stdout: icm.LOG_here("Stdout: " +  self.stdout)
        if self.stderr: icm.LOG_here("Stderr: " +  self.stderr)
        return self


    def out(self):
        G = icm.IcmGlobalContext()
        icm.ANN_here(G.icmMyFullName() + ':' + str(self.invokerName) + ':' + ucf.stackFrameInfoGet(2))
        if self.stdcmnd: icm.ANN_write("Stdcmnd: \n" +  self.stdcmnd)
        if self.stdout: icm.ANN_write("Stdout: ")
        if self.stdout: icm.OUT_write(self.stdout)
        if self.stderr: icm.ANN_write("Stderr: \n" +  self.stderr)
        return self


"""
*  [[elisp:(org-cycle)][| ]]  [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(beginning-of-buffer)][Top]] [[elisp:(delete-other-windows)][(1)]] || Func             ::  opSuccess    [[elisp:(org-cycle)][| ]]
"""
def opSuccess():
    """."""
    return (
        Outcome()
    )


####+BEGIN: bx:dblock:python:class :className "BasicOp" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /BasicOp/ object  [[elisp:(org-cycle)][| ]]
"""
class BasicOp(object):
####+END:
    """
** Basic Operation.
"""

    opVisibility = ["all"]  # users, developers, internal
    opUsers = []            # lsipusr
    opGroups = []           # bystar
    opImpact = []           # read, modify

    def __init__(self,
                 outcome=None,
                 log=0,
    ):
        self.outcome = outcome
        self.log = log

    def docStrClass(self,):
        return self.__class__.__doc__

    def users(self,):
        return self.__class__.opUsers

    def groups(self,):
        return self.__class__.opGroups

    def impact(self,):
        return self.__class__.opImpact

    def visibility(self,):
        return self.__class__.opVisibility

    def getOutcome(self):
        if self.outcome:
            return self.outcome
        return Outcome(invokerName=self.myName())

    def opMyName(self):
        return self.__class__.__name__

    def myName(self):
        return self.opMyName()


####+BEGIN: bx:dblock:python:class :className "AbstractWithinOpWrapper" :classType "basic"
"""
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Class-basic :: /AbstractWithinOpWrapper/ object  [[elisp:(org-cycle)][| ]]
"""
class AbstractWithinOpWrapper(object):
####+END:
    """
** Basic Operation.
"""

    opVisibility = ["all"]  # users, developers, internal
    opUsers = []            # lsipusr
    opGroups = []           # bystar
    opImpact = []           # read, modify

    def __init__(self,
                 invedBy=None,
                 log=0,
    ):
        self.invedBy = invedBy
        if invedBy:
            self.outcome = invedBy.cmndOutcome
        else:
            self.outcome = None
        self.log = log

    def docStrClass(self,):
        return self.__class__.__doc__

    def users(self,):
        return self.__class__.opUsers

    def groups(self,):
        return self.__class__.opGroups

    def impact(self,):
        return self.__class__.opImpact

    def visibility(self,):
        return self.__class__.opVisibility

    def getOutcome(self):
        if self.outcome:
            return self.outcome
        return Outcome(invokerName=self.myName())

    def opMyName(self):
        return self.__class__.__name__

    def myName(self):
        return self.opMyName()



####+BEGIN: bx:icm:python:section :title "End Of Editable Text"
"""
*  [[elisp:(beginning-of-buffer)][Top]] ############## [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] [[elisp:(delete-other-windows)][(1)]]    *End Of Editable Text*  [[elisp:(org-cycle)][| ]]  [[elisp:(org-show-subtree)][|=]]
"""
####+END:

####+BEGIN: bx:dblock:global:file-insert-cond :cond "./blee.el" :file "/bisos/apps/defaults/software/plusOrg/dblock/inserts/endOfFileControls.org"
#+STARTUP: showall
####+END:
