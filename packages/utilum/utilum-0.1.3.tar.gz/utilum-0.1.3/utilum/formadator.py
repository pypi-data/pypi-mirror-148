# Form Validator

class ValidatorLevel1Django:
    def __init__(self, request):
        self.request = request
        self.attrEntity = self.request.POST
        self.absentList = []
        self.emptyList = []
        self.inValidList = []

        self.absentDict = {}
        self.emptyDict = {}

    def addAttr(self, level1AttrName, allowEmpty = False):
        attrEntity = self.attrEntity

        combinedName = f"{level1AttrName}"
        # print("combinedName1: ", combinedName,level1AttrName, attrEntity,level1AttrName in self.attrEntity)
        if (level1AttrName in self.attrEntity):
            # print("combinedName2: ", combinedName)
            self.absentDict[combinedName] = False
            trimmedValue = str(attrEntity[level1AttrName]).replace(" ", "")
            if(allowEmpty == False):
                if(len(trimmedValue)==0):
                    self.emptyDict[combinedName] = True
                    self.emptyList.append({
                combinedName: {
                    "message": "Value Empty",
                    "param": combinedName,
                    "location": "POST",
                }})
                else:
                    self.emptyDict[combinedName] = False
            if(allowEmpty == True):
                if(len(trimmedValue)==0):
                    self.emptyDict[combinedName] = True
                else:
                    # print("combinedName: ", combinedName)
                    self.emptyDict[combinedName] = False
        else:
            self.absentDict[combinedName] = True
            self.absentList.append({
                combinedName: {
                    "message": "Attribute Absent",
                    "param": combinedName,
                    "location": "POST",
                }})

    def addRule(self, level1AttrName, ruleFunction):
        ruleEntity = self.request.POST[level1AttrName]

        [ ruleStatus, suggestionMessage ] = ruleFunction(ruleEntity)

        combinedName = f"{level1AttrName}"
        if (ruleStatus == True):pass
        else:
            self.inValidList.append({
                combinedName: {
                    "message": 'Invalid Value',
                    "suggestion": suggestionMessage,
                    "param": combinedName,
                    "location": "POST",
                }})

    def isAbsent(self):
        if(len(self.absentList)>0):return True
        else:return False
    def isEmpty(self):
        if(len(self.emptyList)>0):return True
        else:return False
    def isInvalid(self):
        if(len(self.inValidList)>0):return True
        else:return False

    def isValid(self):
        if(self.isAbsent()):return self.absentList
        elif(self.isEmpty()):return self.emptyList
        elif(self.isInvalid()):return self.inValidList
        else:return True
        

class ValidatorLevel1:
    def __init__(self, request, location):
        self.request = request
        self.location = location
        self.absentList = []
        self.emptyList = []
        self.inValidList = []

    def addAttr(self, level1AttrName, allowEmpty = False):
        if(self.location in self.request):
            attrEntity = self.request[self.location]
        else:
            attrEntity = None

        self.attrEntity = attrEntity
        combinedName = f"{level1AttrName}"
        if (level1AttrName in self.attrEntity):
            if(allowEmpty == False):
                trimmedValue = str(attrEntity[level1AttrName]).replace(" ", "")
                if(len(trimmedValue)==0):
                    self.emptyList.append({
                combinedName: {
                    "message": "Value Empty",
                    "param": combinedName,
                    "location": self.location,
                }})
        else:
            self.absentList.append({
                combinedName: {
                    "message": "Attribute Absent",
                    "param": combinedName,
                    "location": self.location,
                }})

    def addRule(self, level1AttrName, ruleFunction):
        if(self.location in self.request):
            ruleEntity = self.request[self.location][level1AttrName]
        else:
            ruleEntity = None

        [ ruleStatus, suggestionMessage ] = ruleFunction(ruleEntity)

        combinedName = f"{level1AttrName}"
        if (ruleStatus == True):pass
        else:
            self.inValidList.append({
                combinedName: {
                    "message": 'Invalid Value',
                    "suggestion": suggestionMessage,
                    "param": combinedName,
                    "location": self.location,
                }})

    def isAbsent(self):
        if(len(self.absentList)>0):return True
        else:return False
    def isEmpty(self):
        if(len(self.emptyList)>0):return True
        else:return False
    def isInvalid(self):
        if(len(self.inValidList)>0):return True
        else:return False


class ValidatorLevel2:
    def __init__(self, request, location):
        self.request = request
        self.location = location
        self.absentList = []
        self.emptyList = []
        self.inValidList = []

    def addAttr(self, level1AttrName, level2AttrName, allowEmpty = False):
        if(self.location in self.request):
            attrEntity = self.request[self.location][level1AttrName]
        else:
            attrEntity = None

        self.attrEntity = attrEntity
        combinedName = f"{level1AttrName}/{level2AttrName}"
        if (level2AttrName in self.attrEntity):
            if(allowEmpty == False):
                trimmedValue = str(attrEntity[level2AttrName]).replace(" ", "")
                if(len(trimmedValue)==0):
                    self.emptyList.append({
                combinedName: {
                    "message": "Value Empty",
                    "param": combinedName,
                    "location": self.location,
                }})
        else:
            self.absentList.append({
                combinedName: {
                    "message": "Attribute Absent",
                    "param": combinedName,
                    "location": self.location,
                }})        

    def addRule(self, level1AttrName, level2AttrName, ruleFunction):
        if(self.location in self.request):
            ruleEntity = self.request[self.location][level1AttrName][level2AttrName]
        else:
            ruleEntity = None

        [ ruleStatus, suggestionMessage ] = ruleFunction(ruleEntity)

        combinedName = f"{level1AttrName}/{level2AttrName}"
        if (ruleStatus == True):pass
        else:
            self.inValidList.append({
                combinedName: {
                    "message": 'Invalid Value',
                    "suggestion": suggestionMessage,
                    "param": combinedName,
                    "location": self.location,
                }})

    def isAbsent(self):
        if(len(self.absentList)>0):return True
        else:return False
    def isEmpty(self):
        if(len(self.emptyList)>0):return True
        else:return False
    def isInvalid(self):
        if(len(self.inValidList)>0):return True
        else:return False