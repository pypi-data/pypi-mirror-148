class Excercise:
    def __init__(self, exc):
        self.exc = exc
        self.tasks = {}
        pass

    def addTask(self, task):
        self.tasks[f"{task.task}.{task.subtask}"] = task

    def getTasks(self):
        return self.tasks

    def getTaskNo(self):
        return len(self.tasks)
    
    def getPoints(self):
        x = 0
        for t in self.tasks.values():
            x += t.getPoints()
        return x

    def __str__(self) -> str:
        return f"Übung {self.exc}, {self.getTaskNo()} Aufgaben, {self.getPoints()} Punkte"

class Task:
    def __init__(self, exc, task, subtask, points, scores={}):
        '''
        This class manages the state of the excercises.
        Example for arguments:
        ÜB 1, Aufgabe 2.3 a), 2 Punkte 
            exc = 1
            task = 2
            subtask = 3a)
            points = 2

        Args:
            exc(int): Excercise (ÜB), example: 1
            task(int): Task (Aufgabe), example: 2
            subtask(str): Subtask (Teilaufgabe), example: 3a)
            points(float): Points (Punkte), example: 2
        '''
        self.exc = exc
        self.task = task
        self.subtask = subtask
        self.points = points
        self.scores = scores

        exc.addTask(self)

    def __str__(self):
        return self.getTaskInfo()

    def getTaskInfo(self): 
        return f"Aufgabe {self.task}.{self.subtask}, {self.points} Punkte"
        
    def getPoints(self):
        return self.points

    def setSolution(self, solution):
        self.solution = solution
    
    def getSolution(self):
        return self.solution

    def getScores(self):
        return self.scores
