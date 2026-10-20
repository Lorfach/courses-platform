import { useCallback, useEffect, useState, useRef } from 'react';
import Lesson from './Lesson_block/Lesson';
import { apiRequest } from '../api';
import { useMyContext } from '../MyContext';

function Wrapper() {
  const [config, setConfig] = useState(null);
  const hasFetched = useRef(false);
  const { subject } = useMyContext();

  const sortKey = (item) => {
    const title = item.title || "";
    let match;

    if ((match = title.match(/Урок №(\d+)/))) {
      return [0, -parseInt(match[1], 10)];
    }
    if ((match = title.match(/Пробник №(\d+)/))) {
      return [1, -parseInt(match[1], 10)];
    }
    if ((match = title.match(/СЕ(\d+)/))) {
      return [2, -parseInt(match[1], 10)];
    }
    if ((match = title.match(/Бонусный урок №(\d+)/))) {
      return [3, -parseInt(match[1], 10)];
    }
    if ((match = title.match(/ИС(\d+)/))) {
      return [4, -parseInt(match[1], 10)];
    }
    return [5, Number.NEGATIVE_INFINITY]; // Остальные уроки в самом низу
  };

  const groupByType = (lessons) => {
    const groups = {
      Уроки: [],
      Пробники: [],
      СЕ: [],
      "Бонусные уроки": [],
      ИС: [],
      Остальные: [],
    };

    lessons.forEach((lesson) => {
      const title = lesson.title || "";
      if (/Урок №\d+/.test(title)) {
        groups["Уроки"].push(lesson);
      } else if (/Пробник №\d+/.test(title)) {
        groups["Пробники"].push(lesson);
      } else if (/СЕ\d+/.test(title)) {
        groups["СЕ"].push(lesson);
      } else if (/Бонусный урок №\d+/.test(title)) {
        groups["Бонусные уроки"].push(lesson);
      } else if (/ИС\d+/.test(title)) {
        groups["ИС"].push(lesson);
      } else {
        groups["Остальные"].push(lesson);
      }
    });

    return groups;
  };

  const fetchData = useCallback(async () => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    try {
      const response = await apiRequest("main_months", {
        body: JSON.stringify({ [subject]: 'TRUE' }),
      });

      const sortedResponse = response.sort((a, b) => {
        const keyA = sortKey(a);
        const keyB = sortKey(b);
        return keyA[0] - keyB[0] || keyA[1] - keyB[1];
      });

      setConfig(groupByType(sortedResponse)); // Группировка данных по типам
    } catch (error) {
      console.error("Ошибка загрузки данных:", error);
      setConfig(null);
    }
  }, [subject]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return (
    <div className='max-w-[1280px] mx-auto'>
      <div className="w-5/6 mx-auto mt-10 rounded-xl min-h-20 flex flex-col gap-10 pb-10">
        {config
          ? Object.entries(config).map(([type, lessons]) => (
              lessons.length > 0 && (
                <div key={type} className="lesson-group">
                  <h2 className="text-xl font-bold mb-8"></h2>
                  <div className="flex flex-wrap gap-6">
                    {lessons.map((lesson) => (
                      <Lesson
                        key={lesson.id}
                        lesson_title={lesson.title}
                        lesson_id={lesson.id}
                        homeworks={lesson.homeworks}
                        process={lesson.already_complited}
                      />
                    ))}
                  </div>
                </div>
              )
            ))
          : <p>{config === null ? "Загрузка..." : "Нет данных"}</p>
        }
      </div>
    </div>
  );
}

export default Wrapper;
