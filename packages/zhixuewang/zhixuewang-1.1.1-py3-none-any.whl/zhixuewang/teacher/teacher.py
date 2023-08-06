from ast import Str
import asyncio
import json
from zhixuewang.models import BasicSubject, Exam, School, StuClass, StuPerson
from zhixuewang.models import ExtendedList
from typing import List, Dict, Union
from zhixuewang.models import Person, Sex, Subject, SubjectScore
from zhixuewang.teacher.tools import order_by_classId, order_by_schoolId
from zhixuewang.teacher.urls import Url
from zhixuewang.teacher.models import ClassSubjectScores, ExamMarkingProgress, ExtraData, Scores, SubjectMarkingProgress, TeaPerson, TopicMarkingProgress, TopicTeacherMarkingProgress
import httpx

from zhixuewang.tools.rank import get_rank_map


class TeacherAccount(TeaPerson):
    """老师账号"""

    def __init__(self, session):
        super().__init__()
        self._session = session
        self._token = None

    def set_base_info(self):
        r = self._session.get(
            Url.TEST_URL,
            headers={
                "referer":
                "https://www.zhixue.com/container/container/teacher/index/"
            })
        json_data = r.json()["teacher"]
        self.email = json_data.get("email")
        self.gender = Sex.BOY if json_data["gender"] == "1" else Sex.GIRL
        self.id = json_data.get("id")
        self.mobile = json_data.get("mobile")
        self.name = json_data.get("name")
        self.roles = json_data["roles"]
        return self

    async def __get_school_exam_classes(self, school_id: str, subject_id: str) -> List[StuClass]:
        async with httpx.AsyncClient(cookies=self._session.cookies) as client:
            r = await client.get(Url.GET_EXAM_SCHOOLS_URL, params={
                "schoolId": school_id,
                "markingPaperId": subject_id
            })
            data = r.json()
            classes = []
            for each in data:
                classes.append(StuClass(
                    id=each["classId"],
                    name=each["className"],
                    school=School(id=each["schoolId"])
                ))
            return classes
    
    def get_school_exam_classes(self, school_id: str, subject_id: str) -> List[StuClass]:
        data = self.__get_school_exam_classes(school_id, subject_id)
        s = asyncio.run(data)
        print(s)
        return s
        
    def get_exam_subjects(self, exam_id: str) -> ExtendedList[Subject]:
        r = self._session.get(Url.GET_EXAM_SUBJECTS_URL, params={
            "examId": exam_id
        })
        data = r.json()["result"]
        subjects = []
        for each in data:
            name = each["subjectName"]
            if name != "总分" and (not each.get("isSubjectGroup")):  # 排除学科组()
                subjects.append(Subject(
                    id=each["topicSetId"],
                    name=each["subjectName"],
                    code=each["subjectCode"],
                    standard_score=each["standScore"]
                ))
        return ExtendedList(sorted(subjects, key=lambda x: x.code, reverse=False))

    def get_exam_detail(self, exam_id: str) -> Exam:
        r = self._session.post(Url.GET_EXAM_DETAIL_URL, data={
            "examId": exam_id
        })
        data = r.json()["result"]
        exam = Exam()
        schools: ExtendedList[School] = ExtendedList()
        for each in data["schoolList"]:
            schools.append(School(
                id=each["schoolId"],
                name=each["schoolName"]
            ))
        exam.id = exam_id
        exam.name = data["exam"]["examName"]
        exam.grade_code = data["exam"]["gradeCode"]

        isCrossExam = data["exam"]["isCrossExam"]
        exam.schools = schools
        exam.status = str(isCrossExam)
        exam.subjects = self.get_exam_subjects(exam_id)
        return exam

    async def __get_class_score(self, class_id: str, subject_id: str) -> ExtendedList[SubjectScore]:
        async with httpx.AsyncClient(cookies=self._session.cookies) as client:
            r = await client.get(
                Url.GET_REPORT_URL,
                params={
                    "type": "export_single_paper_zip",
                    "classId": class_id,
                    "studentNum": "",
                    "topicSetId": subject_id,
                    "topicNumber": "0",
                    "startScore": "0",
                    "endScore": "10000",
                }, timeout=100)
            data = r.json()
            subjectScores: ExtendedList[SubjectScore] = ExtendedList()
            for each in data["result"]:
                subjectScores.append(SubjectScore(
                    score=each["userScore"],
                    person=StuPerson(
                        id=each["userId"],
                        name=each["userName"],
                        clazz=StuClass(id=each["classId"]),
                        code=each["userNum"]
                    ),
                    subject=Subject(
                        id=subject_id,
                        name=each["subjectName"],
                        code=each["subjectCode"],
                        standard_score=each["standScore"]
                    )
                ))
            return subjectScores

    def __set_data(self, subjectScores: ExtendedList[SubjectScore]):
        extraData, has_many_schools = self.__calc_data(subjectScores)
        for each in subjectScores:
            class_id = each.person.clazz.id
            school_id = each.person.clazz.school.id
            score = each.score
            if has_many_schools:
                each.class_rank = extraData.schoolsRankMap[school_id][class_id][score]
                each.grade_rank = extraData.schoolsRankMap[school_id]["all"][score]
                each.exam_rank = extraData.allRankMap[score]
            else:
                each.class_rank = extraData.schoolRankMap[class_id][score]
                each.grade_rank = extraData.schoolRankMap["all"][score]

    def __calc_data(self, subjectScores: ExtendedList[SubjectScore]):
        schoolIdMap = order_by_schoolId(subjectScores)
        extraData = ExtraData(dict(), dict(), dict())
        all_rankMap = get_rank_map([i.score for i in subjectScores])
        if len(schoolIdMap.keys()) == 1:
            # 单校
            extraData.schoolRankMap["all"] = all_rankMap
            classIdMap = order_by_classId(subjectScores)
            for classId, _subjectScores in classIdMap.items():
                cur_rankMap = get_rank_map([i.score for i in _subjectScores])
                extraData.schoolRankMap[classId] = cur_rankMap
            return extraData, False
        else:
            # 多校
            extraData.allRankMap = all_rankMap
            for schoolId, schoolSubjectScores in schoolIdMap.items():
                school_all_rankMap = get_rank_map([i.score for i in schoolSubjectScores])
                extraData.schoolsRankMap[schoolId] = {}
                extraData.schoolsRankMap[schoolId]["all"] = school_all_rankMap
                classIdMap = order_by_classId(schoolSubjectScores)
                for classId, classSubjectScores in classIdMap.items():
                    class_rankMap = get_rank_map([i.score for i in classSubjectScores])
                    extraData.schoolsRankMap[schoolId][classId] = class_rankMap

            return extraData, True
        
    def __calc_total_score(self, data) -> ExtendedList[SubjectScore]:
        personScoreMap = {}
        for subjectScores in data:
            for each in subjectScores:
                person_id = each.person.id
                if person_id not in personScoreMap:
                    personScoreMap[person_id] = []
                personScoreMap[person_id].append(each)
        totalScores = ExtendedList()
        for personSubjectScores in personScoreMap.values():
            totalSubjectScore = SubjectScore(
                score=0,
                subject=Subject(name="总分", standard_score=0),
                person=personSubjectScores[0].person
            )
            for each in personSubjectScores:
                totalSubjectScore.score += each.score
                totalSubjectScore.subject.standard_score += each.subject.standard_score
            totalScores.append(totalSubjectScore)
        totalScores = ExtendedList(
            sorted(totalScores, key=lambda t: t.score, reverse=True))
        return totalScores

    async def __get_scores(self, exam_id: str, force_no_total_score: bool = False):
        exam = self.get_exam_detail(exam_id)

        tasks = []
        for school in exam.schools:
            tasks.append(self.__get_school_exam_classes(school.id, exam.subjects[0].id))
        result = await asyncio.gather(*tasks)
        classes: ExtendedList[StuClass] = ExtendedList()
        for data in result:
            classes.extend(data)

        class_name_map = {}
        class_school_map = {}

        for clazz in classes:
            class_name_map[clazz.id] = clazz.name
            class_school_map[clazz.id] = exam.schools.find_by_id(clazz.school.id)
        

        class_ids = ",".join([i.id for i in classes])

        tasks = []
        for subject in exam.subjects:
            tasks.append(self.__get_class_score(class_ids, subject.id))
        scores: ExtendedList[ExtendedList[SubjectScore]] = await asyncio.gather(*tasks)
        for each_subject in scores:
            for each in each_subject:
                each.person.clazz.name = class_name_map[each.person.clazz.id]
                each.person.clazz.school = class_school_map[each.person.clazz.id]
            self.__set_data(each_subject)
        if (not force_no_total_score) and len(exam.subjects) > 1:
            total_scores = self.__calc_total_score(scores)
            self.__set_data(total_scores)
            scores.append(total_scores)
        return scores


    def get_scores(self, exam_id: str) -> Scores:
        """获取所有分数

        Args:
            exam_id (str): 考试id

        Returns:
            ExtendedList[ExtendedList[SubjectScore]]
        """
        import time
        st = time.time()
        scores = asyncio.run(self.__get_scores(exam_id))
        print(time.time() - st)
        return Scores(scores)

    def _parse_marking_progress_data(self, r, subject_id: str):
        data = r.json()["message"]
        progress_data = []
        for each in json.loads(data):
            topic_progress_data = TopicMarkingProgress(
                disp_title=each["dispTitle"],
                topic_number=each["topicNum"],
                complete_precent=each["completeRate"],
                subject_id=subject_id
            )
            for each2 in each["teacherList"]:
                topic_progress_data.teachers.append(TopicTeacherMarkingProgress(
                    teacher_name=each2["name"],
                    school=School(
                        id=each2["schoolId"],
                        name=each2["schoolName"]
                    ),
                    is_online=each2["isOnline"],
                    teacher_code=each2["code"],
                    complete_count=each2["completeCount"],
                    uncomplete_count=each2["arUncompleteCount"]
                ))
            progress_data.append(topic_progress_data)
        return progress_data

    def get_marking_progress(self, subject_id: str, school_id: str = ""):
        r = self._session.post(Url.GET_MARKING_PROGRESS_URL, data={
            "progressParam": json.dumps({
                "markingPaperId": subject_id,
                "topicNum": None,
                "subTopicIndex": None,
                "topicStartNum": None,
                "schoolId": school_id,
                "topicProgress": "",
                "teacherProgress": "",
                "isOnline": "",
                "teacherName": "",
                "userId": "",
                "examId": ""
            })
        })
        return self._parse_marking_progress_data(r, subject_id)
        

    async def _get_marking_progress_async(self, subject_id: str, school_id: str):
        async with httpx.AsyncClient(cookies=self._session.cookies) as client:
            r = await client.post(Url.GET_MARKING_PROGRESS_URL, data={
                "progressParam": json.dumps({
                    "markingPaperId": subject_id,
                    "topicNum": None,
                    "subTopicIndex": None,
                    "topicStartNum": None,
                    "schoolId": school_id,
                    "topicProgress": "",
                    "teacherProgress": "",
                    "isOnline": "",
                    "teacherName": "",
                    "userId": "",
                    "examId": ""
                })
            })
            return self._parse_marking_progress_data(r, subject_id)

    def get_token(self) -> str:
        if self._token is not None:
            return self._token
        r = self._session.get("https://www.zhixue.com/container/app/token/getToken")
        self._token = r.json()["result"]
        return self._token

    def get_headers(self):
        return {"token": self.get_token()}

    async def _get_exam_all_marking_progress(self, exam: Exam) -> ExamMarkingProgress:
        tasks = []
        for subject in exam.subjects:
            for school in exam.schools:
                tasks.append(self._get_marking_progress_async(subject.id, school.id))
        result = await asyncio.gather(*tasks)
        examMarkingProgress = ExamMarkingProgress(exam)
        for each in result:
            examMarkingProgress.markingProgresses.append(SubjectMarkingProgress(
                subject=exam.subjects.find_by_id(each[0].subject_id),  # type: ignore
                markingProgresses=each
            ))
        return examMarkingProgress
        
    def get_exam_all_marking_progress(self, exam_id: str) -> ExamMarkingProgress:
        exam = self.get_exam_detail(exam_id)
        return asyncio.run(self._get_exam_all_marking_progress(exam))
        