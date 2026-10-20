import { createContext, useContext, useState, useEffect, useCallback, useMemo } from "react";
import { Navigate, useParams } from "react-router-dom";
import { apiRequest, getCookie } from "./api";


export const MyContext = createContext({});
// console.log(2);

export const MyProvider = ({ children }) => {
  const token = getCookie('token');
  const { subject_ } = useParams();
  // console.log(lessonId);
  // console.log(homeworkId);



  if (!token || token === 'undefined') {
    return <Navigate to="/login" replace />;
  }

  const [answerInput, setAnswerInput] = useState('');
  const [questionNumber, setQuestionNumber] = useState(0);
  const [subject, setSubject] = useState(subject_);
  const [inputBlock, setInputBlock] = useState(null)
  const [questions, setQuestions] = useState([]);


  useEffect(() => {
    setAnswerInput('');
  }, [questionNumber]);


  useEffect(() => {
    return () => {
      setAnswerInput('');
    };
  }, []);


  const memoizedSetAnswerInput = useCallback(setAnswerInput, []);
  const memoizedSetQuestionNumber = useCallback(setQuestionNumber, []);
  const memoizedSetSubject = useCallback(setSubject, [])
  const memoizedSetInputBlock = useCallback(setInputBlock, [])
  const memoizedSetQuestions = useCallback(setQuestions, [])
  // const memoizedSetThisQuestion = useCallback(setThisQuestion, [])
  const sendAnswer = useCallback(async (folder, question, answer_id, answ, is_correct, subject_) => {
    setQuestions(prev => {
      const updatedQuestions = [...prev];
      updatedQuestions[questionNumber] = {
        ...updatedQuestions[questionNumber],
        answer2: answ,
        correct: is_correct,
      };
      return updatedQuestions;
    });

    await apiRequest("answer_to_bd", {
      body: JSON.stringify({ folder, question, answer_id, answer: answ, correct: is_correct, subject: subject_ }),
    });
  }, [questionNumber]);


  const contextValue = useMemo(() => ({
    answerInput,
    setAnswerInput: memoizedSetAnswerInput,
    questionNumber,
    setQuestionNumber: memoizedSetQuestionNumber,
    subject,
    setSubject: memoizedSetSubject,
    sendAnswer,
    inputBlock,
    setInputBlock: memoizedSetInputBlock,
    questions,
    setQuestions: memoizedSetQuestions
  }), [answerInput, questionNumber, subject, inputBlock, questions, memoizedSetAnswerInput, memoizedSetQuestionNumber, memoizedSetSubject, memoizedSetInputBlock, memoizedSetQuestions]);

  return (
    <MyContext.Provider value={contextValue}>
      {children}
    </MyContext.Provider>
  );
};


export function useMyContext() {
  return useContext(MyContext);
}
