// 문항별로 작성한 해설을 복습 카드로 구성한다. 주제명으로 사실을 추정하지 않는다.
// 동일한 원문을 사용하므로 해설을 수정하면 핵심노트에도 함께 반영된다.
(function () {
  "use strict";
  const marks = "①②③④⑤";
  const types = {
    exception: ["해당하지 않는 설명 찾기", "맞는 사실과 틀린 연결을 구분하기"],
    order: ["사건 순서 정리", "사건마다 연도·왕대를 붙여 순서 말하기"],
    timeline: ["연표 구간 찾기", "사건의 연도와 양쪽 경계 사건을 함께 말하기"],
    interval: ["두 사건 사이 찾기", "양 끝 사건을 확정하고 그 사이 사건 말하기"],
    period: ["기준 시기와 사건 대조", "자료의 기준 시기와 보기 사건의 연도를 대조하기"],
    relative: ["기준 사건의 앞뒤 구분", "기준 사건보다 앞인지 뒤인지 설명하기"],
    picture: ["사진·작품 구별", "이름과 눈에 보이는 특징을 함께 떠올리기"],
    combination: ["연결·조합 비교", "각 연결을 따로 판단한 뒤 맞는 조합 만들기"],
    identify: ["대상과 특징 연결", "단서로 대상을 찾고 비슷한 대상과 구별하기"]
  };

  function kind(q, figure) {
    if (/옳지|적절하지|없는 것은/.test(q.q)) return "exception";
    if (/순서/.test(q.q)) return "order";
    if (/연표/.test(q.q)) return "timeline";
    if (/사이/.test(q.q)) return "interval";
    if (/이후|이전/.test(q.q)) return "relative";
    if (figure?.choices) return "picture";
    if (/<보기>|ㄱ[.．]/.test(q.ctx)) return "combination";
    return "identify";
  }

  // 날짜의 소수점이나 ① 같은 보기 표시는 문장 경계로 취급하지 않는다.
  function shortFact(text) {
    return text.split(/(?<=[.!?])\s+/u).slice(0, 2).join(" ");
  }

  window.buildQuestionCoreNotes = function (questions, explanations, figures = {}, timelines = {}) {
    const result = {};
    for (const q of questions) {
      const id = q.r + "-" + q.n;
      const source = explanations[id];
      if (!source) continue; // 오래된 파일 조합에서도 기존 주제 노트를 표시할 수 있다.
      const figure = figures[id];
      const inferred = kind(q, figure);
      const type = timelines[id] && inferred === "identify" ? "period" : inferred;
      const [task, recallGoal] = types[type];
      result[id] = {
        id, round: q.r, number: q.n, era: q.era, topic: q.topic,
        title: `제${q.r}회 ${q.n}번 · ${q.topic}`,
        type, task, recallGoal,
        anchors: source.clues.slice(),
        timeline: (timelines[id] || []).map(row => row.slice()),
        takeaway: source.takeaway,
        connections: q.ch.map((choice, i) => ({
          number: i + 1,
          cue: figure?.choices?.[i]?.name || choice,
          // ‘사진 특징’으로만 확인된 자료에 작가나 시대를 새로 붙이지 않는다.
          descriptive: figure?.choices?.[i]?.nameStatus === "description",
          fact: shortFact(source.choices[i]),
          detail: source.choices[i],
          selected: i + 1 === q.a,
          label: marks[i]
        }))
      };
    }
    return result;
  };
})();
