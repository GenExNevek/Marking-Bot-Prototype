
-- @block Table Template

CREATE TABLE Template (
  TemplateID INT PRIMARY KEY,
  QuestionType VARCHAR(255),
  CourseID INT,
  Description VARCHAR(255),
  FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- @block Table Users

CREATE TABLE Users (
  UserID INT PRIMARY KEY,
  Name VARCHAR(255),
  Email VARCHAR(255),
  Role VARCHAR(255),
  PasswordHash VARCHAR(255)
);

-- @block Table Courses
CREATE TABLE Courses (
  CourseID INT PRIMARY KEY,
  CourseTitle VARCHAR(255)
);

-- @block Table Modules

CREATE TABLE Modules (
  ModuleNo INT PRIMARY KEY,
  CourseID INT,
  ModuleTitle VARCHAR(255),
  FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
);

-- @block Table Assignments

CREATE TABLE Assignments (
  AssignmentID INT PRIMARY KEY,
  ModuleNo INT,
  AssignmentDescription TEXT,
  FOREIGN KEY (ModuleNo) REFERENCES Modules(ModuleNo)
);

-- @block Table AssignmentOutput

CREATE TABLE AssignmentOutput (
  AssignmentOutputID INT PRIMARY KEY,
  AssignmentID INT,
  AssignmentCommentsAndEvidence TEXT,
  AssignmentAchievedStatus BOOLEAN,
  FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID)
);

-- @block Table LearningObjectives

CREATE TABLE LearningObjectives (
  LearningObjectiveNo INT PRIMARY KEY,
  AssignmentID INT,
  LearningObjectiveDescription VARCHAR(255),
  TaskNo INT,
  FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID)
);

-- @block Table Tasks

CREATE TABLE Tasks (
  TaskNo INT PRIMARY KEY,
  AssignmentID INT,
  TaskDescription VARCHAR(255),
  FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID)
);

-- @block Table LearningObjectivesTasks

CREATE TABLE LearningObjectivesTasks (
  TaskNo INT,
  LearningObjectiveNo INT,
  PRIMARY KEY (TaskNo, LearningObjectiveNo),
  FOREIGN KEY (TaskNo) REFERENCES Tasks(TaskNo),
  FOREIGN KEY (LearningObjectiveNo) REFERENCES LearningObjectives(LearningObjectiveNo)
);

-- @block Table Questions

CREATE TABLE Questions (
  QuestionNo INT PRIMARY KEY,
  TaskNo INT,
  QuestionCriteria VARCHAR(255),
  QuestionDescription VARCHAR(255),
  FOREIGN KEY (TaskNo) REFERENCES Tasks(TaskNo)
);

-- @block Table QuestionRelationships

CREATE TABLE QuestionRelationships (
  RelationshipID INT PRIMARY KEY,
  QuestionNo1 INT,
  QuestionNo2 INT,
  FOREIGN KEY (QuestionNo1) REFERENCES Questions(QuestionNo),
  FOREIGN KEY (QuestionNo2) REFERENCES Questions(QuestionNo)
);

-- @block Table Figures

CREATE TABLE Figures (
  FigureID INT PRIMARY KEY,
  FigureDescription VARCHAR(255)
);

-- @block Table QuestionFigures

CREATE TABLE QuestionFigures (
  QuestionNo INT,
  FigureID INT,
  PRIMARY KEY (QuestionNo, FigureID),
  FOREIGN KEY (QuestionNo) REFERENCES Questions(QuestionNo),
  FOREIGN KEY (FigureID) REFERENCES Figures(FigureID)
);

-- @block Table SuggestedEvidence

CREATE TABLE SuggestedEvidence (
  EvidenceID INT PRIMARY KEY,
  QuestionNo INT,
  EvidenceDescription TEXT,
  FOREIGN KEY (QuestionNo) REFERENCES Questions(QuestionNo)
);

-- @block Table StudentSubmissions

CREATE TABLE StudentSubmissions (
  SubmissionID INT PRIMARY KEY,
  UserID INT,
  QuestionNo INT,
  SubmissionContent TEXT,
  FOREIGN KEY (UserID) REFERENCES Users(UserID),
  FOREIGN KEY (QuestionNo) REFERENCES Questions(QuestionNo)
);

-- @block Table QuestionOutput
CREATE TABLE QuestionOutput (
  QuestionOutputID INT AUTO_INCREMENT PRIMARY KEY,
  SubmissionID INT,
  QuestionNo INT,
  QuestionCommentsAndEvidence TEXT,
  QuestionAchievedStatus VARCHAR(255),
  FOREIGN KEY (SubmissionID) REFERENCES StudentSubmissions(SubmissionID),
  FOREIGN KEY (QuestionNo) REFERENCES Questions(QuestionNo)
);

-- @block Table TaskOutput
CREATE TABLE TaskOutput (
  TaskOutputID INT AUTO_INCREMENT PRIMARY KEY,
  TaskNo INT,
  TaskCommentsAndEvidence TEXT,
  TaskAchievedStatus BOOLEAN,
  FOREIGN KEY (TaskNo) REFERENCES Tasks(TaskNo)
);

-- @block Table AssignmentAndTaskOutput
CREATE TABLE AssignmentAndTaskOutput (
  AssignmentOutputID INT,
  TaskOutputID INT,
  PRIMARY KEY (AssignmentOutputID, TaskOutputID),
  FOREIGN KEY (AssignmentOutputID) REFERENCES AssignmentOutput(AssignmentOutputID),
  FOREIGN KEY (TaskOutputID) REFERENCES TaskOutput(TaskOutputID)
);

-- @block Table TaskAndQuestionOutput
CREATE TABLE TaskAndQuestionOutput (
  QuestionOutputID INT,
  TaskOutputID INT,
  PRIMARY KEY (TaskOutputID, QuestionOutputID),
  FOREIGN KEY (QuestionOutputID) REFERENCES QuestionOutput(QuestionOutputID),
  FOREIGN KEY (TaskOutputID) REFERENCES TaskOutput(TaskOutputID)
);