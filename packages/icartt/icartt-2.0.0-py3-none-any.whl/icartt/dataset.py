import datetime
import sys
import pathlib
import collections
import re
import warnings
from enum import IntEnum

import numpy as np

from . import utils

DEFAULT_NUM_FORMAT = "%g"
"""Default number format for output. Provides the `fmt` parameter of :func:`numpy.savetxt` internally."""

DEFAULT_FIELD_DELIM = ","
"""Default field delimiter"""

DEFAULT_SCALE_FACTOR = 1.0
"""Default variable scale factor"""

DEFAULT_MISSING_VALUE = -9999.0
"""Default variable missing value"""


class Formats(IntEnum):
    """ICARTT File Format Indices (FFI)"""

    FFI1001 = 1001
    FFI2110 = 2110


class VariableType(IntEnum):
    """ICARTT Variable Types"""

    IndependentVariable = 1
    IndependentBoundedVariable = 2
    AuxiliaryVariable = 3
    DependentVariable = 4


class DataStore1001:
    """Data model for FFI1001"""

    def __init__(self, ivar, dvars):

        self.ivarname = ivar.shortname

        self.varnames = [ivar.shortname] + [x for x in dvars]
        self.missingValues = {x: dvars[x].miss for x in dvars}
        self.missingValues.update({self.ivarname: ivar.miss})

        self.default_dtype = np.float64

        self.dtypes = [(name, self.default_dtype) for name in self.varnames]

        self.data = None

    def __getitem__(self, s=slice(None)):
        # we can only slice if we have something, so
        if self.data is not None:
            return self.data[s]
        # returns None implicitly if self.data is None

    def addFromTxt(self, f, delimiter, max_rows=None):
        # genfromtxt would warn if file is empty. We do not want that.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            newData = np.genfromtxt(
                f,
                names=self.varnames,
                dtype=self.dtypes,
                missing_values=self.missingValues,
                usemask=True,
                delimiter=delimiter,
                max_rows=max_rows,
                deletechars="",
            ).filled(fill_value=np.nan)
        self.add(newData)

    def add(self, newData):
        """(bulk) add data, providing a (structured) numpy array.

        Array has to have shape [ (ivar, dvar, dvar, ...), ... ],
        missing values have to be set to :obj:`numpy.nan`.

        :param newData: data to be added
        :type newData: numpy.ndarray
        """
        if not isinstance(newData, np.ndarray):
            raise TypeError("Input data needs to be numpy ndarray.")

        workData = newData.copy()
        if workData.dtype.names is None:
            try:
                workData.dtype = [(name, workData.dtype) for name in self.varnames]
            except:
                ValueError(
                    "Could not assign names to data structure, are you providing an array containing all variables?"
                )

        if self.data is None:
            self.data = workData
        else:
            self.data = np.append(self.data, workData)

    def denanify(self, d):
        dd = d.copy()
        for k, miss in self.missingValues.items():
            dd[k][np.isnan(dd[k])] = miss
        return dd

    def write(
        self, f=sys.stdout, fmt=DEFAULT_NUM_FORMAT, delimiter=DEFAULT_FIELD_DELIM
    ):
        # TODO the fact that we need to clean before writing suggests we need to be more careful what to "add" in the first place!
        d = self.denanify(self.data)
        # single line data is 0D if passed as tuple, savetxt cannot work with 0D. Make 1D.
        if d.ndim == 0:
            d = np.array([d])
        # need to squeeze extra dimension added for one liners added as np.array
        if len(d.shape) == 2:
            d = np.squeeze(d, axis=1)

        np.savetxt(f, d, fmt=fmt, delimiter=delimiter)


class DataStore2110(collections.UserDict):
    """Data model for FFI2110"""

    def __init__(self, ivar, ibvar, auxvars, dvars):

        self.ivarname = ivar.shortname
        self.ibvarname = ibvar.shortname

        self.auxvarnames = [x for x in auxvars]
        self.dvarnames = [x for x in dvars]

        self.missingValues = {x: dvars[x].miss for x in dvars}
        self.missingValues.update({x: auxvars[x].miss for x in auxvars})
        self.missingValues.update({self.ibvarname: ibvar.miss})
        self.missingValues.update({self.ivarname: ivar.miss})

        self.nauxvarname = self.auxvarnames[0]  # convention!

        self.data = {}

        self.ivar = ivar
        self.auxvars = auxvars
        self.ibvar = ibvar
        self.dvars = dvars

    def __getitem__(self, s=slice(None)):
        # we can only slice if we have something, so
        if self.data is not None:
            return self.data[s]
        # returns None implicitly if self.data is None

    def addFromTxt(self, f, delimiter):
        while f:
            auxds = DataStore1001(self.ivar, self.auxvars)
            depds = DataStore1001(self.ibvar, self.dvars)
            try:
                auxds.addFromTxt(f, delimiter, max_rows=1)
            except:
                # we are at the end of the file if this happens
                break

            ndeprows = int(auxds[self.nauxvarname])

            # it is indeed possible to have zero dependent data lines
            if ndeprows > 0:
                try:
                    depds.addFromTxt(f, delimiter, max_rows=ndeprows)
                except:
                    raise IOError("Could not read dependent data lines.")

            ivarValue = float(auxds[self.ivar.shortname])

            self.data[ivarValue] = {"AUX": auxds, "DEP": depds}

    def add(self, newAuxData, newDepData):
        """(bulk) add data, providing (structured) numpy arrays for both the auxiliary and dependent data line(s)
        for a given ivar value.

        Arrays have to have shape [ (ivar, auxvar, auxvar, ...) ] and
        [ (ibvar, depvar, depvar, ...), ... ] for auxiliary and dependent data line(s), respectively.
        missing values have to be set to :obj:`numpy.nan`.

        :param newAuxData: auxiliary data line to be added
        :type newAuxData: numpy.ndarray

        :param newDepData: auxiliary data line(s) to be added
        :type newDepData: numpy.ndarray
        """
        auxds = DataStore1001(self.ivar, self.auxvars)
        depds = DataStore1001(self.ibvar, self.dvars)

        auxds.add(newAuxData)
        depds.add(newDepData)

        ivarValue = float(auxds[self.ivar.shortname])

        self.data[ivarValue] = {"AUX": auxds, "DEP": depds}

    def write(
        self,
        f=sys.stdout,
        fmt_aux=DEFAULT_NUM_FORMAT,
        fmt_dep=DEFAULT_NUM_FORMAT,
        delimiter_aux=DEFAULT_FIELD_DELIM,
        delimiter_dep=DEFAULT_FIELD_DELIM,
    ):
        for ivarvalue in self.data:
            self.data[ivarvalue]["AUX"].write(f, fmt=fmt_aux, delimiter=delimiter_aux)
            self.data[ivarvalue]["DEP"].write(f, fmt=fmt_dep, delimiter=delimiter_dep)


class KeywordComment:
    def __init__(self, key, naAllowed):
        self.key = key
        self.naAllowed = naAllowed
        self.data = []

    def append(self, data):
        self.data.append(data)

    def __str__(self):
        d = "\n".join(self.data) if self.data else "N/A"
        return self.key + ": " + d


class StandardNormalComments(collections.UserList):
    @property
    def nlines(self):
        """calculates the number of lines in the normal comments section"""
        # shortnames line is always there:
        n = 1
        # freeform comment might or might not be there:
        n += sum(len(s.split("\n")) for s in self.freeform)
        # tagged comments have at least one line:
        for k in self.keywords.values():
            n += sum(len(s.split("\n")) for s in k.data) or 1
        return n

    @property
    def data(self):
        return (
            self.freeform + [str(s) for s in self.keywords.values()] + [self.shortnames]
        )

    def ingest(self, raw):
        # last line is always shortname
        self.shortnames = raw.pop()

        # per standard: The free-form text section consists of the lines
        # between the beginning of the normal comments section
        # and the first required keyword. [...] The required “KEYWORD: value” pairs block
        # starts with the line that begins with the first required keyword
        # and must include all required “KEYWORD: value” pairs
        # in the order listed in the ICARTT documentation.

        currentKeyword = None
        keywordLine = False
        for l in raw:
            possibleKeyword = l.split(":")[0].strip()
            if possibleKeyword in self.keywords or re.match(
                "R[a-zA-Z0-9]{1,2}[ ]*", possibleKeyword
            ):
                currentKeyword = possibleKeyword
                keywordLine = True
                if not currentKeyword in self.keywords:  # for the revisions only...
                    self.keywords[currentKeyword] = KeywordComment(
                        currentKeyword, False
                    )
            else:
                keywordLine = False

            if currentKeyword is None:
                self.freeform.append(l)
            elif keywordLine:
                self.keywords[currentKeyword].append(
                    l.replace(l.split(":")[0] + ":", "").strip()
                )
            else:
                self.keywords[currentKeyword].append(l.strip())

        for key in self.keywords:
            if not self.keywords[key].data:
                warnings.warn(
                    f"Normal comments: required keyword {str(key)} is missing."
                )

    def __init__(self):
        self.freeform = []
        self.shortnames = []

        requiredKeywords = (
            "PI_CONTACT_INFO",
            "PLATFORM",
            "LOCATION",
            "ASSOCIATED_DATA",
            "INSTRUMENT_INFO",
            "DATA_INFO",
            "UNCERTAINTY",
            "ULOD_FLAG",
            "ULOD_VALUE",
            "LLOD_FLAG",
            "LLOD_VALUE",
            "DM_CONTACT_INFO",
            "PROJECT_INFO",
            "STIPULATIONS_ON_USE",
            "OTHER_COMMENTS",
            "REVISION",
        )

        self.keywords = {k: KeywordComment(k, True) for k in requiredKeywords}

        self.keywords["UNCERTAINTY"].naAllowed = False
        self.keywords["REVISION"].naAllowed = False

    def __str__(self):
        return "\n".join(f"{str(v)}" for v in self.keywords.values())


class Variable:
    """An ICARTT variable description with name, units, scale and missing value."""

    def desc(self, delimiter=DEFAULT_FIELD_DELIM):
        """Variable description string as it appears in an ICARTT file

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional

        :return: description string
        :rtype: str
        """
        descstr = [str(self.shortname), str(self.units)]
        if self.standardname is not None:
            descstr += [str(self.standardname)]
        if self.longname is not None:
            descstr += [str(self.longname)]
        return delimiter.join(descstr)

    def isValidVariablename(self, name):
        # ICARTT Standard v2 2.1.1 2)
        # Variable short names and variable standard names:
        # Uppercase and lowercase ASCII alphanumeric characters
        # and underscores.

        allAreAlphaOrUnderscore = all(re.match("[a-zA-Z0-9_]", c) for c in name)
        # The first character must be a letter,
        firstIsAlpha = bool(re.match("[a-zA-Z]", name[0]))
        # and the name can be at most 31 characters in length.
        le31Chars = len(name) <= 31

        return allAreAlphaOrUnderscore and firstIsAlpha and le31Chars

    def __init__(
        self,
        shortname,
        units,
        standardname,
        longname,
        vartype=VariableType.DependentVariable,
        scale=DEFAULT_SCALE_FACTOR,
        miss=DEFAULT_MISSING_VALUE,
    ):
        """
        :param shortname: Short name of the variable
        :type shortname: str

        :param units: Units of the variable
        :type units: str

        :param standardname: Standard name of the variable
        :type standardname: str

        :param longname: Long name of the variable
        :type longname: str

        :param vartype: Variable type (unbounded/bounded independent or dependent), defaults to `VariableType.dependentVariable`
        :type vartype: VariableType, optional

        :param scale: Scaling factor for the variable, defaults to DEFAULT_SCALE_FACTOR
        :type scale: float, optional

        :param miss: Missing value for the variable, defaults to DEFAULT_MISSING_VALUE
        :type miss: float, optional
        """
        if not self.isValidVariablename(shortname):
            warnings.warn(
                f"Variable short name {str(shortname)} does not comply with ICARTT standard v2"
            )

        self.shortname = shortname
        self.units = units
        self.standardname = standardname
        self.longname = longname
        self.vartype = vartype
        self.scale = scale
        self.miss = miss

    def __repr__(self):
        return f"[{self.units}], {self.vartype.name}"

    def __str__(self):
        return self.desc()


class Dataset:
    """An ICARTT dataset that can be created from scratch or read from a file,
    manipulated, and then written to a file.
    """

    @property
    def nHeader(self):
        """Header line count

        :return: line count
        :rtype: int
        """
        total = -1
        if self.format == Formats.FFI1001:
            total = (
                14
                + len(self.dependentVariables)
                + len(self.specialComments)
                + self.normalComments.nlines
            )
        if self.format == Formats.FFI2110:
            # 2: IVAR + IBVAR
            total = (
                16
                + 2
                + len(self.auxiliaryVariables)
                + len(self.dependentVariables)
                + len(self.specialComments)
                + self.normalComments.nlines
            )
        return total

    @property
    def times(self):
        """Time steps of the data

        :return: array of time steps
        :rtype: numpy.ndarray
        """

        if self.defineMode:
            return np.datetime64("NaT")

        # for 1001 it's an array, for 2110 a dict
        if not isinstance(self.data.data, (np.ndarray, dict)):
            return np.datetime64("NaT")

        # it is possible to have an empty dict
        if isinstance(self.data.data, dict) and not self.data.data:
            return np.datetime64("NaT")

        ref_dt = np.datetime64(datetime.datetime(*self.dateOfCollection), "ns")

        time_values = []
        if self.format == Formats.FFI1001:
            time_values = self.data[self.independentVariable.shortname]
        elif self.format == Formats.FFI2110:
            # for 2110, data keys are independent variable values by definition in out implementation
            time_values = np.array(list(self.data.keys()))
        else:
            raise NotImplementedError(
                "times method not implemented for this ICARTT format!"
            )

        # ivar unit is seconds as per standard; need to convert to ns to use timedelta64[ns] type.
        return ref_dt + (time_values * 10**9).astype("timedelta64[ns]")

    @property
    def variables(self):
        """Variables (independent + dependent + auxiliary)

        :return: dictionary of all variables
        :rtype: dict
        """
        variables = {}

        if self.independentVariable is not None:
            variables[self.independentVariable.shortname] = self.independentVariable
        if self.independentBoundedVariable is not None:
            variables[
                self.independentBoundedVariable.shortname
            ] = self.independentBoundedVariable

        variables = {**variables, **self.dependentVariables, **self.auxiliaryVariables}

        return variables

    def readHeader(self, delimiter=DEFAULT_FIELD_DELIM):
        """Read the ICARTT header (from file)

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """
        if self.inputFhandle:
            if self.inputFhandle.closed:
                self.inputFhandle = open(self.inputFhandle.name, encoding="utf-8")
            f = utils.FilehandleWithLinecounter(self.inputFhandle, delimiter)
            self._readHeader(f)
            self.inputFhandle.close()

    def _readHeader(self, f):
        # line 1 - Number of lines in header, file format index (most files use
        # 1001) - comma delimited.
        dmp = f.readline()

        nHeaderSuggested = int(dmp[0])

        try:
            self.format = Formats(int(dmp[1]))
        except ValueError as ve:
            raise NotImplementedError(f"ICARTT format {dmp[1]} not implemented") from ve

        if len(dmp) > 2:
            self.version = dmp[2]

        # line 2 - PI last name, first name/initial.
        self.PIName = f.readline(doSplit=False)

        # line 3 - Organization/affiliation of PI.
        self.PIAffiliation = f.readline(doSplit=False)

        # line 4 - Data source description (e.g., instrument name, platform name,
        # model name, etc.).
        self.dataSourceDescription = f.readline(doSplit=False)

        # line 5 - Mission name (usually the mission acronym).
        self.missionName = f.readline(doSplit=False)

        # line 6 - File volume number, number of file volumes (these integer values
        # are used when the data require more than one file per day; for data that
        # require only one file these values are set to 1, 1) - comma delimited.
        dmp = f.readline()
        self.fileVolumeNumber = int(dmp[0])
        self.totalNumberOfFileVolumes = int(dmp[1])

        # line 7 - UTC date when data begin, UTC date of data reduction or revision
        # - comma delimited (yyyy, mm, dd, yyyy, mm, dd).
        dmp = f.readline()
        self.dateOfCollection = tuple(map(int, dmp[:3]))
        self.dateOfRevision = tuple(map(int, dmp[3:6]))

        # line 8 - Data Interval (This value describes the time spacing (in seconds)
        # between consecutive data records. It is the (constant) interval between
        # values of the independent variable. For 1 Hz data the data interval value
        # is 1 and for 10 Hz data the value is 0.1. All intervals longer than 1
        # second must be reported as Start and Stop times, and the Data Interval
        # value is set to 0. The Mid-point time is required when it is not at the
        # average of Start and Stop times. For additional information see Section
        # 2.5 below.).
        dmp = f.readline()
        # might have multiple entries for 2110
        self.dataIntervalCode = [float(x) for x in dmp]

        # line 9 - Description or name of independent variable (This is the name
        # chosen for the start time. It always refers to the number of seconds UTC
        # from the start of the day on which measurements began. It should be noted
        # here that the independent variable should monotonically increase even when
        # crossing over to a second day.

        if self.format == Formats.FFI2110:
            dmp = f.readline()
            shortname, units, standardname, longname = utils.extractVardesc(dmp)
            self.independentBoundedVariable = Variable(
                shortname,
                units,
                standardname,
                longname,
                vartype=VariableType.IndependentBoundedVariable,
            )

        dmp = f.readline()
        shortname, units, standardname, longname = utils.extractVardesc(dmp)
        self.independentVariable = Variable(
            shortname,
            units,
            standardname,
            longname,
            vartype=VariableType.IndependentVariable,
        )

        def readVars(f, vtype):
            # line 10 - Number of variables (Integer value showing the number of
            # dependent variables: the total number of columns of data is this value
            # plus one.).
            nvar = int(f.readline()[0])

            # line 11- Scale factors (1 for most cases, except where grossly
            # inconvenient) - comma delimited.
            vscale = [x for x in f.readline()]

            # line 12 - Missing data indicators (This is -9999 (or -99999, etc.) for
            # any missing data condition, except for the main time (independent)
            # variable which is never missing) - comma delimited.
            vmiss = [x for x in f.readline()]
            # no float casting here, as we need to do string comparison lateron when reading data...

            # line 13 - Variable names and units (Short variable name and units are
            # required, and optional long descriptive name, in that order, and separated
            # by commas. If the variable is unitless, enter the keyword "none" for its
            # units. Each short variable name and units (and optional long name) are
            # entered on one line. The short variable name must correspond exactly to
            # the name used for that variable as a column header, i.e., the last header
            # line prior to start of data.).
            dmp = f.readline()
            shortname, units, standardname, longname = utils.extractVardesc(dmp)
            vshortname = [shortname]
            vunits = [units]
            vstandardname = [standardname]
            vlongname = [longname]

            for _ in range(1, nvar):
                dmp = f.readline()
                shortname, units, standardname, longname = utils.extractVardesc(dmp)
                vshortname += [shortname]
                vunits += [units]
                vstandardname += [standardname]
                vlongname += [longname]

            d = {}
            for shortname, unit, standardname, longname, scale, miss in zip(
                vshortname, vunits, vstandardname, vlongname, vscale, vmiss
            ):
                d[shortname] = Variable(
                    shortname,
                    unit,
                    standardname,
                    longname,
                    scale=scale,
                    miss=miss,
                    vartype=vtype,
                )

            return d

        self.dependentVariables = readVars(f, VariableType.DependentVariable)

        if self.format == Formats.FFI2110:
            self.auxiliaryVariables = readVars(f, VariableType.AuxiliaryVariable)

        # line 14 + nvar - Number of SPECIAL comment lines (Integer value
        # indicating the number of lines of special comments, NOT including this
        # line.).
        nscom = int(f.readline()[0])

        # line 15 + nvar - Special comments (Notes of problems or special
        # circumstances unique to this file. An example would be comments/problems
        # associated with a particular flight.).
        self.specialComments = [f.readline(doSplit=False) for _ in range(nscom)]

        # line 16 + nvar + nscom - Number of Normal comments (i.e., number of
        # additional lines of SUPPORTING information: Integer value indicating the
        # number of lines of additional information, NOT including this line.).
        nncom = int(f.readline()[0])

        # line 17 + nvar + nscom - Normal comments (SUPPORTING information: This is
        # the place for investigators to more completely describe the data and
        # measurement parameters. The supporting information structure is described
        # below as a list of key word: value pairs. Specifically include here
        # information on the platform used, the geo-location of data, measurement
        # technique, and data revision comments. Note the non-optional information
        # regarding uncertainty, the upper limit of detection (ULOD) and the lower
        # limit of detection (LLOD) for each measured variable. The ULOD and LLOD
        # are the values, in the same units as the measurements that correspond to
        # the flags -7777's and -8888's within the data, respectively. The last line
        # of this section should contain all the "short" variable names on one line.
        # The key words in this section are written in BOLD below and must appear in
        # this section of the header along with the relevant data listed after the
        # colon. For key words where information is not needed or applicable, simply
        # enter N/A.).
        rawNcom = [f.readline(doSplit=False) for _ in range(nncom)]
        self.normalComments.ingest(rawNcom)

        r = self.normalComments.keywords["REVISION"].data
        r = "0" if not r else r[0].strip("R")
        self.revision = r

        self.nHeaderFile = f.line

        # TODO this warning might be missleading since it assumes all normalComment keywords
        #      had been defined - which is not guaranteed.
        if self.nHeader != nHeaderSuggested:
            warnings.warn(
                f"Number of header lines suggested in line 1 ({int(nHeaderSuggested)}) do not match actual header lines read ({int(self.nHeader)})"
            )

    def readData(self, delimiter=DEFAULT_FIELD_DELIM):
        """Read ICARTT data (from file)

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """
        if self.inputFhandle:
            if self.inputFhandle.closed:
                self.inputFhandle = open(self.inputFhandle.name, encoding="utf-8")

            for _ in range(self.nHeaderFile):
                self.inputFhandle.readline()

            self.data.addFromTxt(self.inputFhandle, delimiter)
            self.inputFhandle.close()

    def read(self, delimiter=DEFAULT_FIELD_DELIM):
        """Read ICARTT data and header

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """
        self.readHeader(delimiter)
        self.endDefineMode()
        self.readData(delimiter)

    def makeFileName(self, dateFormat="%Y%m%d"):
        """Create ICARTT-compliant file name based on the information contained in the dataset

        :param dateFormat: date format to use when parsing, defaults to '%Y%m%d'
        :type dateFormat: str, optional

        :return: file name generated
        :rtype: str
        """
        fn = (
            self.dataID
            + "_"
            + self.locationID
            + "_"
            + datetime.datetime.strftime(
                datetime.datetime(*self.dateOfCollection), dateFormat
            )
        )
        fn += "_R" + str(self.revision) if not self.revision is None else ""
        fn += "_L" + str(self.launch) if not self.launch is None else ""
        fn += (
            "_V" + str(self.fileVolumeNumber)
            if self.totalNumberOfFileVolumes > 1
            else ""
        )

        return fn + ".ict"

    def isValidFileName(self, name):
        """test whether file name complies with ICARTT standard:

        ICARTT standard v2 2.1.1 3)

        Filename: Uppercase and lowercase ASCII alphanumeric characters (i.e. A-Z, a-z, 0-9), underscore, period, and hyphen. File names can be a maximum 127 characters in length.

        :param name: file name
        :type name: str

        :return: is file name valid according to ICARTT standard?
        :rtype: bool
        """
        allAsciiAlpha = all(re.match("[a-zA-Z0-9-_.]", c) for c in name)
        lessThan128Characters = len(name) < 128

        return allAsciiAlpha and lessThan128Characters and name.endswith(".ict")

    def writeHeader(self, f=sys.stdout, delimiter=DEFAULT_FIELD_DELIM):
        """Write header

        :param f: `file object <https://docs.python.org/3/glossary.html#term-file-object>`_ to write to, defaults to sys.stdout
        :type f: handle, optional

        :param delimiter: field delimiter character(s) for output, defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """

        def write_to_file(txt):
            f.write(str(txt) + "\n")

        # Number of lines in header, file format index (most files use 1001) - comma delimited.
        versInfo = [self.nHeader, self.format.value]
        if self.version is not None:
            versInfo.append(self.version)
        txt = delimiter.join([str(x) for x in versInfo])

        write_to_file(txt)
        # PI last name, first name/initial.
        write_to_file(self.PIName)
        # Organization/affiliation of PI.
        write_to_file(self.PIAffiliation)
        # Data source description (e.g., instrument name, platform name, model name, etc.).
        write_to_file(self.dataSourceDescription)
        # Mission name (usually the mission acronym).
        write_to_file(self.missionName)
        # File volume number, number of file volumes (these integer values are used when the data require more than one file per day; for data that require only one file these values are set to 1, 1) - comma delimited.
        write_to_file(
            delimiter.join(
                [str(self.fileVolumeNumber), str(self.totalNumberOfFileVolumes)]
            )
        )
        # UTC date when data begin, UTC date of data reduction or revision - comma delimited (yyyy, mm, dd, yyyy, mm, dd).
        write_to_file(
            delimiter.join(
                f"{x:02d}" for x in (*self.dateOfCollection, *self.dateOfRevision)
            )
        )
        # Data Interval (This value describes the time spacing (in seconds) between consecutive data records. It is the (constant) interval between values of the independent variable. For 1 Hz data the data interval value is 1 and for 10 Hz data the value is 0.1. All intervals longer than 1 second must be reported as Start and Stop times, and the Data Interval value is set to 0. The Mid-point time is required when it is not at the average of Start and Stop times. For additional information see Section 2.5 below.).
        write_to_file(delimiter.join([str(x) for x in self.dataIntervalCode]))
        if self.format == Formats.FFI2110:
            # Description or name of independent (bound) variable (This is the name chosen for the start time. It always refers to the number of seconds UTC from the start of the day on which measurements began. It should be noted here that the independent variable should monotonically increase even when crossing over to a second day.).
            write_to_file(self.independentBoundedVariable.desc(delimiter))
        # Description or name of independent variable (This is the name chosen for the start time. It always refers to the number of seconds UTC from the start of the day on which measurements began. It should be noted here that the independent variable should monotonically increase even when crossing over to a second day.).
        write_to_file(self.independentVariable.desc(delimiter))
        # Number of variables (Integer value showing the number of dependent variables: the total number of columns of data is this value plus one.).
        write_to_file(len(self.dependentVariables))
        # Scale factors (1 for most cases, except where grossly inconvenient) - comma delimited.
        write_to_file(
            delimiter.join(
                [str(DVAR.scale) for DVAR in self.dependentVariables.values()]
            )
        )
        # Missing data indicators (This is -9999 (or -99999, etc.) for any missing data condition, except for the main time (independent) variable which is never missing) - comma delimited.
        write_to_file(
            delimiter.join(
                [str(DVAR.miss) for DVAR in self.dependentVariables.values()]
            )
        )
        # Variable names and units (Short variable name and units are required, and optional long descriptive name, in that order, and separated by commas. If the variable is unitless, enter the keyword "none" for its units. Each short variable name and units (and optional long name) are entered on one line. The short variable name must correspond exactly to the name used for that variable as a column header, i.e., the last header line prior to start of data.).
        for DVAR in self.dependentVariables.values():
            write_to_file(DVAR.desc(delimiter))

        if self.format == Formats.FFI2110:
            # Number of variables (Integer value showing the number of dependent variables: the total number of columns of data is this value plus one.).
            write_to_file(len(self.auxiliaryVariables))
            # Scale factors (1 for most cases, except where grossly inconvenient) - comma delimited.
            write_to_file(
                delimiter.join(
                    [str(AUXVAR.scale) for AUXVAR in self.auxiliaryVariables.values()]
                )
            )
            # Missing data indicators (This is -9999 (or -99999, etc.) for any missing data condition, except for the main time (independent) variable which is never missing) - comma delimited.
            write_to_file(
                delimiter.join(
                    [str(AUXVAR.miss) for AUXVAR in self.auxiliaryVariables.values()]
                )
            )
            # Variable names and units (Short variable name and units are required, and optional long descriptive name, in that order, and separated by commas. If the variable is unitless, enter the keyword "none" for its units. Each short variable name and units (and optional long name) are entered on one line. The short variable name must correspond exactly to the name used for that variable as a column header, i.e., the last header line prior to start of data.).
            for AUXVAR in self.auxiliaryVariables.values():
                write_to_file(AUXVAR.desc(delimiter))

        # Number of SPECIAL comment lines (Integer value indicating the number of lines of special comments, NOT including this line.).
        write_to_file(f"{len(self.specialComments)}")
        # Special comments (Notes of problems or special circumstances unique to this file. An example would be comments/problems associated with a particular flight.).
        for x in self.specialComments:
            write_to_file(x)
        # Number of Normal comments (i.e., number of additional lines of SUPPORTING information: Integer value indicating the number of lines of additional information, NOT including this line.).
        write_to_file(f"{self.normalComments.nlines}")
        # Normal comments (SUPPORTING information: This is the place for investigators to more completely describe the data and measurement parameters. The supporting information structure is described below as a list of key word: value pairs. Specifically include here information on the platform used, the geo-location of data, measurement technique, and data revision comments. Note the non-optional information regarding uncertainty, the upper limit of detection (ULOD) and the lower limit of detection (LLOD) for each measured variable. The ULOD and LLOD are the values, in the same units as the measurements that correspond to the flags -7777s and -8888s within the data, respectively. The last line of this section should contain all the short variable names on one line. The key words in this section are written in BOLD below and must appear in this section of the header along with the relevant data listed after the colon. For key words where information is not needed or applicable, simply enter N/A.).
        # re-create last line out of actual data if missing...
        if not self.normalComments.shortnames:
            self.normalComments.shortnames = delimiter.join(
                [self.variables[x].shortname for x in self.variables]
            )
        for x in self.normalComments:
            write_to_file(x)

    def writeData(
        self, f=sys.stdout, fmt=DEFAULT_NUM_FORMAT, delimiter=DEFAULT_FIELD_DELIM
    ):
        """Write data

        :param f: `file object <https://docs.python.org/3/glossary.html#term-file-object>`_ to write to, defaults to sys.stdout
        :type f: handle, optional

        :param fmt: format string for output, accepts anything :func:`numpy.savetxt` would, defaults to DEFAULT_NUM_FORMAT
        :type fmt: str or sequence of str, optional

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """
        if self.format == Formats.FFI1001:
            self.data.write(f=f, fmt=fmt, delimiter=delimiter)
        elif self.format == Formats.FFI2110:
            self.data.write(
                f=f,
                fmt_aux=fmt,
                delimiter_aux=delimiter,
                fmt_dep=fmt,
                delimiter_dep=delimiter,
            )
        else:
            raise NotImplementedError("Unknown FFI!")

    def write(
        self, f=sys.stdout, fmt=DEFAULT_NUM_FORMAT, delimiter=DEFAULT_FIELD_DELIM
    ):
        """Write header and data

        :param f: `file object <https://docs.python.org/3/glossary.html#term-file-object>`_ to write to, defaults to sys.stdout
        :type f: handle, optional

        :param fmt: format string for output, accepts anything :func:`numpy.savetxt` would, defaults to DEFAULT_NUM_FORMAT
        :type fmt: str or sequence of str, optional

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional
        """
        self.writeHeader(f=f, delimiter=delimiter)
        self.writeData(f=f, fmt=fmt, delimiter=delimiter)

    def endDefineMode(self):
        """Fixes the variables structure of the dataset. Sets up the data store,
        so data can be added. Needs to be called after variable definition
        and before adding data.
        """
        self.defineMode = False

        # create data store
        if self.format == Formats.FFI1001:
            self.data = DataStore1001(self.independentVariable, self.dependentVariables)
        elif self.format == Formats.FFI2110:
            self.data = DataStore2110(
                self.independentVariable,
                self.independentBoundedVariable,
                self.auxiliaryVariables,
                self.dependentVariables,
            )

    def __del__(self):
        if self.inputFhandle:
            if not self.inputFhandle.closed:
                self.inputFhandle.close()

    def __str__(self):
        s = [
            f"ICARTT Dataset {self.makeFileName()}, format index {self.format.value}",
            f"data ID: {self.dataID}",
            f"location ID: {self.locationID}",
            f"PI: {self.PIName}",
            f"Affiliation: {self.PIAffiliation}",
            f"Mission: {self.missionName}",
            f"Collection date, Revision date: {self.dateOfCollection}, {self.dateOfRevision}",
            f"Variables ({len(self.variables)}):\n{', '.join(x for x in self.variables)}",
        ]
        return "\n".join(s)

    def __init__(
        self,
        f=None,
        loadData=True,
        delimiter=DEFAULT_FIELD_DELIM,
        format=Formats.FFI1001,
    ):
        """
        :param f: file path or file handle to use, defaults to None
        :type f: str or `file object <https://docs.python.org/3/glossary.html#term-file-object>`_, optional

        :param loadData: whether to load data as well (or only header if False), defaults to `True`
        :type loadData: bool, optional

        :param delimiter: field delimiter character(s), defaults to DEFAULT_FIELD_DELIM
        :type delimiter: str, optional

        :param format: ICARTT file format to create, defaults to 1001
        :type format: Formats, optional
        """

        self.format = format
        self.version = None  # TODO: should this be 2.0 by default?

        self.dataID = "dataID"
        self.locationID = "locationID"

        self.revision = 0
        self.launch = None
        self.fileVolumeNumber = 1
        self.totalNumberOfFileVolumes = 1

        self.PIName = "Mustermann, Martin"
        self.PIAffiliation = "Musterinstitut"
        self.dataSourceDescription = "Musterdatenprodukt"
        self.missionName = "MUSTEREX"

        # .utcnow() should not be used in general, but it is ok if you just need the timetuple.
        self.dateOfCollection = datetime.datetime.utcnow().timetuple()[:3]
        self.dateOfRevision = datetime.datetime.utcnow().timetuple()[:3]
        self.dataIntervalCode = [0.0]

        self.independentVariable = None
        self.independentBoundedVariable = None
        self.auxiliaryVariables = {}
        self.dependentVariables = {}

        self.specialComments = []
        self.normalComments = StandardNormalComments()

        # Standard v2.0 for normal comments requires all keywords present,
        # might not be the case - then reading data will fail
        self.nHeaderFile = -1

        self.data = None

        self.defineMode = True

        self.inputFhandle = None

        # read data if f is not None
        if f is not None:
            if isinstance(f, (str, pathlib.Path)):
                self.inputFhandle = open(f, "r", encoding="utf-8")
            else:
                self.inputFhandle = f

            if not self.isValidFileName(pathlib.Path(f).name):
                warnings.warn(f"{pathlib.Path(f).name} is not a valid ICARTT filename")
            else:
                # try to obtain dataID and locationID from file name
                parts = pathlib.Path(f).name.split("_")
                # there should be at least 3 parts; data ID, location ID and revision date + file name extension
                if len(parts) > 2:
                    self.dataID = parts[0]
                    self.locationID = parts[1]

            self.readHeader(delimiter)
            if loadData:
                self.endDefineMode()
                self.readData(delimiter)
