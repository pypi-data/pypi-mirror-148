import logging
import operator
import os
import sys
import pkgutil
import argparse
import requests
import jsonpickle
from zipfile import ZipFile
from distutils.dir_util import mkpath
from abc import ABC
from abc import abstractmethod

######## START CONTENT ########
def INVALID_NAME():
    return "INVALID_NAME"


#Self registration for use with json loading.
#Any class that derives from SelfRegistering can be instantiated with:
#   SelfRegistering("ClassName")
#Based on: https://stackoverflow.com/questions/55973284/how-to-create-this-registering-factory-in-python/55973426
class SelfRegistering(object):

    class ClassNotFound(Exception): pass

    def __init__(this, *args, **kwargs):
        #ignore args.
        super().__init__()

    @classmethod
    def GetSubclasses(cls):
        for subclass in cls.__subclasses__():
            # logging.info(f"Subclass dict: {subclass.__dict__}")
            yield subclass
            for subclass in subclass.GetSubclasses():
                yield subclass

    #TODO: How do we pass args to the subsequently called __init__()?
    def __new__(cls, classname, *args, **kwargs):
        for subclass in cls.GetSubclasses():
            if subclass.__name__ == classname:
                logging.debug(f"Creating new {subclass.__name__}")

                # Using "object" base class method avoids recursion here.
                child = object.__new__(subclass)

                #__dict__ is always blank during __new__ and only populated by __init__.
                #This is only useful as a negative control.
                # logging.debug(f"Created object of {child.__dict__}")

                return child
        
        # no subclass with matching classname found (and no default defined)
        raise SelfRegistering.ClassNotFound(f"No known SelfRegistering class: {classname}")

    @staticmethod
    def RegisterAllClassesInDirectory(directory):
        logging.debug(f"Loading SelfRegistering classes in {directory}")
        # logging.debug(f"Available files: {os.listdir(directory)}")
        for importer, file, _ in pkgutil.iter_modules([directory]):
            logging.debug(f"Found {file} with {importer}")
            if file not in sys.modules and file != 'main':
                module = importer.find_module(file).load_module(file)


#A Datum is a base class for any object-oriented class structure.
#This class is intended to be derived from and added to.
#The members of this class are helpful labels along with the ability to invalidate a datum.
class Datum(SelfRegistering):

    #Don't worry about this.
    #If you really want to know, look at SelfRegistering.
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(this, name=INVALID_NAME(), number=0):
        # logging.debug("init Datum")

        #Names are generally useful.
        this.name = name

        #Storing validity as a member makes it easy to generate bad return values (i.e. instead of checking for None) as well as manipulate class (e.g. each analysis step invalidates some class and all invalid class are discarded at the end of analysis).
        this.valid = True 

    #Override this if you have your own validity checks.
    def IsValid(this):
        return this.valid == True

    #Sets valid to true
    #Override this if you have members you need to handle with care.
    def MakeValid(this):
        this.valid = True

    #Sets valid to false.
    def Invalidate(this):
        this.valid = False


#A DataContainer allows Data to be stored and worked with.
#This class is intended to be derived from and added to.
#Each DataContainer is comprised of multiple Data (see Datum.py for more).
#NOTE: DataContainers are, themselves Data. Thus, you can nest your child classes however you would like.
class DataContainer(Datum):
    def __init__(this, name=INVALID_NAME()):
        super().__init__(name)
        this.data = []

    #RETURNS: an empty, invalid Datum.
    def InvalidDatum(this):
        ret = Datum()
        ret.Invalidate()
        return ret

    #Sort things! Requires by be a valid attribute of all Data.
    def SortData(this, by):
        this.data.sort(key=operator.attrgetter(by))

    #Adds a Datum to *this
    def AddDatum(this, datum):
        this.data.append(datum)

    #RETURNS: a Datum with datumAttribute equal to match, an invalid Datum if none found.
    def GetDatumBy(this, datumAttribute, match):
        for d in this.data:
            try: #within for loop 'cause maybe there's an issue with only 1 Datum and the rest are fine.
                if (str(getattr(d, datumAttribute)) == str(match)):
                    return d
            except Exception as e:
                logging.error(f"{this.name} - {e.message}")
                continue
        return this.InvalidDatum()

    #RETURNS: a Datum of the given name, an invalid Datum if none found.
    def GetDatum(this, name):
        return this.GetDatumBy('name', name)

    #Removes all Data in toRem from *this.
    #RETURNS: the Data removed
    def RemoveData(this, toRem):
        # logging.debug(f"Removing {toRem}")
        this.data = [d for d in this.data if d not in toRem]
        return toRem

    #Removes all Data which match toRem along the given attribute
    def RemoveDataBy(this, datumAttribute, toRem):
        toRem = [d for d in this.data if str(getattr(d, datumAttribute)) in list(map(str, toRem))]
        return this.RemoveData(toRem)

    #Removes all Data in *this except toKeep.
    #RETURNS: the Data removed
    def KeepOnlyData(this, toKeep):
        toRem = [d for d in this.data if d not in toKeep]
        return this.RemoveData(toRem)

    #Removes all Data except those that match toKeep along the given attribute
    #RETURNS: the Data removed
    def KeepOnlyDataBy(this, datumAttribute, toKeep):
        # logging.debug(f"Keeping only class with a {datumAttribute} of {toKeep}")
        # toRem = []
        # for d in this.class:
        #     shouldRem = False
        #     for k in toKeep:
        #         if (str(getattr(d, datumAttribute)) == str(k)):
        #             logging.debug(f"found {k} in {d.__dict__}")
        #             shouldRem = True
        #             break
        #     if (shouldRem):
        #         toRem.append(d)
        #     else:
        #         logging.debug(f"{k} not found in {d.__dict__}")
        toRem = [d for d in this.data if str(getattr(d, datumAttribute)) not in list(map(str, toKeep))]
        return this.RemoveData(toRem)

    #Removes all Data with the name "INVALID NAME"
    #RETURNS: the removed Data
    def RemoveAllUnlabeledData(this):
        toRem = []
        for d in this.data:
            if (d.name =="INVALID NAME"):
                toRem.append(d)
        return this.RemoveData(toRem)

    #Removes all invalid Data
    #RETURNS: the removed Data
    def RemoveAllInvalidData(this):
        toRem = []
        for d in this.data:
            if (not d.IsValid()):
                toRem.append(d)
        return this.RemoveData(toRem)

    #Removes all Data that have an attribute value relative to target.
    #The given relation can be things like operator.le (i.e. <=)
    #   See https://docs.python.org/3/library/operator.html for more info.
    #If ignoreNames is specified, any Data of those names will be ignored.
    #RETURNS: the Data removed
    def RemoveDataRelativeToTarget(this, datumAttribute, relation, target, ignoreNames = []):
        try:
            toRem = []
            for d in this.data:
                if (ignoreNames and d.name in ignoreNames):
                    continue
                if (relation(getattr(d, datumAttribute), target)):
                    toRem.append(d)
            return this.RemoveData(toRem)
        except Exception as e:
            logging.error(f"{this.name} - {e.message}")
            return []

    #Removes any Data that have the same datumAttribute as a previous Datum, keeping only the first.
    #RETURNS: The Data removed
    def RemoveDuplicateDataOf(this, datumAttribute):
        toRem = [] #list of Data
        alreadyProcessed = [] #list of strings, not whatever datumAttribute is.
        for d1 in this.data:
            skip = False
            for dp in alreadyProcessed:
                if (str(getattr(d1, datumAttribute)) == dp):
                    skip = True
                    break
            if (skip):
                continue
            for d2 in this.data:
                if (d1 is not d2 and str(getattr(d1, datumAttribute)) == str(getattr(d2, datumAttribute))):
                    logging.info(f"Removing duplicate Datum {d2} with unique id {getattr(d2, datumAttribute)}")
                    toRem.append(d2)
                    alreadyProcessed.append(str(getattr(d1, datumAttribute)))
        return this.RemoveData(toRem)

    #Adds all Data from otherDataContainer to *this.
    #If there are duplicate Data identified by the attribute preventDuplicatesOf, they are removed.
    #RETURNS: the Data removed, if any.
    def ImportDataFrom(this, otherDataContainer, preventDuplicatesOf=None):
        this.data.extend(otherDataContainer.data);
        if (preventDuplicatesOf is not None):
            return this.RemoveDuplicateDataOf(preventDuplicatesOf)
        return []


class MissingArgumentError(Exception):
    pass


#UserFunctor is a base class for any function-oriented class structure or operation.
#This class derives from Datum, primarily, to give it a name but also to allow it to be stored and manipulated, should you so desire.
class UserFunctor(ABC, Datum):

    def __init__(this, name=INVALID_NAME()):
        super().__init__(name)
        this.requiredKWArgs = []

    #Override this and do whatever!
    #This is purposefully vague.
    @abstractmethod
    def UserFunction(this, **kwargs):
        raise NotImplementedError 

    #Override this with any additional argument validation you need.
    #This is called before PreCall(), below.
    def ValidateArgs(this, **kwargs):
        logging.debug(f"kwargs: {kwargs}")
        logging.debug(f"required kwargs: {this.requiredKWArgs}")
        for rkw in this.requiredKWArgs:
            if (rkw not in kwargs):
                logging.error(f"argument {rkw} not found in {kwargs}")
                raise MissingArgumentError(f"argument {rkw} not found in {kwargs}") #TODO: not formatting string??

    #Override this with any logic you'd like to run at the top of __call__
    def PreCall(this, **kwargs):
        pass

    #Override this with any logic you'd like to run at the bottom of __call__
    def PostCall(this, **kwargs):
        pass

    #Make functor.
    #Don't worry about this; logic is abstracted to UserFunction
    def __call__(this, **kwargs) :
        logging.debug(f"{this.name}({kwargs})")
        this.ValidateArgs(**kwargs)
        this.PreCall(**kwargs)
        ret = this.UserFunction(**kwargs)
        this.PostCall(**kwargs)
        return ret


#Executor: a base class for user interfaces.
#An Executor is a functor and can be executed as such.
#For example
#   class MyExecutor(Executor):
#       def __init__(this):
#           super().__init__()
#   . . .
#   myprogram = MyExecutor()
#   myprogram()
#NOTE: Diamond inheritance of Datum.
class Executor(DataContainer, UserFunctor):

    def __init__(this, name=INVALID_NAME(), descriptionStr="eons python framework. Extend as thou wilt."):
        this.SetupLogging()

        super().__init__(name)

        this.cwd = os.getcwd()
        this.Configure()
        this.argparser = argparse.ArgumentParser(description = descriptionStr)
        this.args = None
        this.extraArgs = None
        this.AddArgs()


    #Configure class defaults.
    #Override this to customize your Executor.
    def Configure(this):
        this.defaultRepoDirectory = os.path.abspath(os.path.join(this.cwd, "./eons/"))
        this.registerDirectories = []
        this.defualtConfigFile = None


    #Add a place to search for SelfRegistering classes.
    #These should all be relative to the invoking working directory (i.e. whatever './' is at time of calling Executor())
    def RegisterDirectory(this, directory):
        this.registerDirectories.append(os.path.abspath(os.path.join(this.cwd,directory)))


    #Global logging config.
    #Override this method to disable or change.
    def SetupLogging(this):
        logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)', datefmt = '%H:%M:%S')


    #Adds command line arguments.
    #Override this method to change. Optionally, call super().AddArgs() within your method to simply add to this list.
    def AddArgs(this):
        this.argparser.add_argument('--verbose', '-v', action='count', default=0)
        this.argparser.add_argument('--config', '-c', type=str, default=None, help='Path to configuration file containing only valid JSON.', dest='config')
        this.argparser.add_argument('--no-repo', action='store_true', default=False, help='prevents searching online repositories', dest='no_repo')

    #Create any sub-class necessary for child-operations
    #Does not RETURN anything.
    def InitData(this):
        pass


    #Register all classes in each directory in this.registerDirectories
    def RegisterAllClasses(this):
        for d in this.registerDirectories:
            this.RegisterAllClassesInDirectory(os.path.join(os.getcwd(), d))


    #Something went wrong, let's quit.
    #TODO: should this simply raise an exception?
    def ExitDueToErr(this, errorStr):
        # logging.info("#################################################################\n")
        logging.error(errorStr)
        # logging.info("\n#################################################################")
        this.argparser.print_help()
        sys.exit()


    #Populate the configuration details for *this.
    def PopulateConfig(this):
        this.config = None
        if (this.args.config is not None and os.path.isfile(this.args.config)):
            configFile = open(this.args.config, "r")
            this.config = jsonpickle.decode(configFile.read())
            configFile.close()
            logging.debug(f"Got config contents: {this.config}")


    # Get information for how to download packages.
    def PopulateRepoDetails(this):
        details = [
            "store",
            "url",
            "username",
            "password"
        ]
        this.repo = {}

        if (this.args.no_repo is not None and this.args.no_repo):
            for key in details:
                this.repo[key] = None
        else:
            for key in details:
                this.repo[key] = this.Fetch(f"repo_{key}")

            if (this.repo['store'] is None):
                this.repo['store'] = this.defaultRepoDirectory

            if (this.repo['url'] is None):
                this.repo['url'] = "https://api.infrastructure.tech/v1/package"


    #Do the argparse thing.
    #Extra arguments are converted from --this-format to this_format, without preceding dashes. For example, --repo-url ... becomes repo_url ... 
    def ParseArgs(this):
        this.args, extraArgs = this.argparser.parse_known_args()

        extraArgsKeys = []
        for index in range(0, len(extraArgs), 2):
            keyStr = extraArgs[index]
            keyStr.replace('--', '').replace('-', '_')
            extraArgsKeys.append(keyStr)

        extraArgsValues = []
        for index in range(1, len(extraArgs), 2):
            extraArgsValues.append(extraArgs[index])

        this.extraArgs = dict(zip(extraArgsKeys, extraArgsValues))

        if (this.args.verbose > 0): #TODO: different log levels with -vv, etc.?
            logging.getLogger().setLevel(logging.DEBUG)


    # Will try to get a value for the given varName from:
    #    first: this.
    #    second: extra arguments provided to *this.
    #    third: the config file, if provided.
    #    fourth: the environment.
    # RETURNS the value of the given variable or None.
    def Fetch(this, varName):
        logging.debug(f"Fetching {varName}...")

        if (hasattr(this, varName)):
            logging.debug(f"...got {varName} from {this.name}.")
            return getattr(this, varName)

        for key, val in this.extraArgs.items():
            if (key == varName):
                logging.debug(f"...got {varName} from argument.")
                return val

        if (this.config is not None):
            for key, val in this.config.items():
                if (key == varName):
                    logging.debug(f"...got {varName} from config.")
                    return val

        envVar = os.getenv(varName)
        if (envVar is not None):
            logging.debug(f"...got {varName} from environment")
            return envVar

        return None

        
    #UserFunctor required method
    #Override this with your own workflow.
    def UserFunction(this, **kwargs):
        this.ParseArgs() #first, to enable debug and other such settings.
        this.PopulateConfig()
        this.PopulateRepoDetails()
        this.RegisterAllClasses()
        this.InitData()


    #Attempts to download the given package from the repo url specified in calling args.
    #Will refresh registered classes upon success
    #RETURNS void
    #Does not guarantee new classes are made available; errors need to be handled by the caller.
    def DownloadPackage(this, packageName, registerClasses=True, createSubDirectory=False):

        if (this.args.no_repo is not None and this.args.no_repo):
            logging.debug(f"Refusing to download {packageName}; we were told not to use a repository.")
            return

        url = f"{this.repo['url']}/download?package_name={packageName}"

        auth = None
        if this.repo['username'] and this.repo['password']:
            auth = requests.auth.HTTPBasicAuth(this.repo['username'], this.repo['password'])

        packageQuery = requests.get(url, auth=auth)

        if (packageQuery.status_code != 200 or not len(packageQuery.content)):
            logging.error(f"Unable to download {packageName}")
            #TODO: raise error?
            return #let caller decide what to do next.

        if (not os.path.exists(this.repo['store'])):
            logging.debug(f"Creating directory {this.repo['store']}")
            mkpath(this.repo['store'])

        packageZip = os.path.join(this.repo['store'], f"{packageName}.zip")

        logging.debug(f"Writing {packageZip}")
        openPackage = open(packageZip, 'wb+')
        openPackage.write(packageQuery.content)
        openPackage.close()
        if (not os.path.exists(packageZip)):
            logging.error(f"Failed to create {packageZip}")
            # TODO: raise error?
            return

        logging.debug(f"Extracting {packageZip}")
        openArchive = ZipFile(packageZip, 'r')
        extractLoc = this.repo['store']
        if (createSubDirectory):
            extractLoc = os.path.join(extractLoc, packageName)
        openArchive.extractall(f"{extractLoc}")
        openArchive.close()
        os.remove(packageZip)
        
        if (registerClasses):
            this.RegisterAllClassesInDirectory(this.repo['store'])

    #RETURNS and instance of a Datum, UserFunctor, etc. which has been discovered by a prior call of RegisterAllClassesInDirectory()
    def GetRegistered(this, registeredName, prefix=""):

        #Start by looking at what we have.
        try:
            registered = SelfRegistering(registeredName)

        except Exception as e:

            #Then try registering what's already downloaded.
            try:
                this.RegisterAllClassesInDirectory(this.repo['store'])
                registered = SelfRegistering(registeredName)

            except Exception as e2:

                logging.debug(f"{registeredName} not found.")
                packageName = registeredName
                if (prefix):
                    packageName = f"{prefix}_{registeredName}"
                logging.debug(f"Trying to download {packageName} from repository ({this.repo['url']})")
                this.DownloadPackage(packageName)
                registered = SelfRegistering(registeredName)

        #NOTE: UserFunctors are Data, so they have an IsValid() method
        if (not registered or not registered.IsValid()):
            logging.error(f"Could not find {registeredName}")
            raise Exception(f"Could not get registered class for {registeredName}")

        return registered


